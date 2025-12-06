from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from form.models import (
    UserFormSubmission,
    QuestionResponse,
    BaseQuestion,
    Step,
    QuestionCondition,
    StepCondition,
    MRForm,
)

User = get_user_model()

UserType = type[User]

# How often we will allow a question or step to be repeated
MAX_REPEAT_LIMIT = 10


class FormEvaluator:
    """
    Creates a user-specific view of a form, with conditional logic and repeats
    applied, based on a user's last submission.

    Args:
        form: The MRForm config/template being evaluated.
        user: The user for whom the form is being evaluated.
        create_submission: Whether to create a UserFormSubmission if one doesn't exist.
    """

    def __init__(self, form: MRForm, user: UserType, create_submission: bool = False):
        self.form = form
        self.user = user
        self.create_submission = create_submission
        self._submission = None
        self._responses_cache = None

    @property
    def submission(self) -> UserFormSubmission | None:
        """
        Get or optionally create the user's submission.

        For now, this fetches the latest submission; in the future, we will
        want to support multiple submissions per user.
        """
        if self._submission is None:
            if self.create_submission:
                self._submission = UserFormSubmission.objects.create(
                    user=self.user, form=self.form
                )
            else:
                self._submission = (
                    UserFormSubmission.objects.filter(
                        user=self.user,
                        form=self.form,
                    )
                    .order_by("-updated_at")
                    .first()
                )

        return self._submission

    @property
    def responses(self) -> dict[int, list[QuestionResponse]]:
        """Cache all responses for this submission, grouped by question_id."""
        if self._responses_cache is None:
            self._responses_cache = {}
            if self.submission:
                responses = QuestionResponse.objects.filter(
                    submission=self.submission
                ).select_related("question")
                for response in responses:
                    if response.question.pk not in self._responses_cache:
                        self._responses_cache[response.question.pk] = []
                    self._responses_cache[response.question.pk].append(response)
        return self._responses_cache

    def check_trigger_value(self, answer: dict, trigger_value: dict) -> bool:
        """Check if an answer matches the trigger condition."""
        # If trigger_value is {}, the condition is always considered met.
        if not trigger_value:
            return True

        # Number comparisons
        if "min" in trigger_value:
            return answer.get("value", 0) >= trigger_value["min"]
        if "max" in trigger_value:
            return answer.get("value", 0) <= trigger_value["max"]
        if "exact" in trigger_value:
            return answer.get("value") == trigger_value["exact"]

        # Select option checks -- currently: the check passes if *any* of the
        # answer's ids are in the list of ids in trigger_value.
        if "option_ids" in trigger_value:
            user_option_ids = answer.get("option_ids", [])
            if "option_id" in answer:
                user_option_ids = [answer["option_id"]]
            return any(opt in trigger_value["option_ids"] for opt in user_option_ids)

        # Direct value match (for booleans, strings, etc.)
        if "value" in trigger_value:
            return answer.get("value") == trigger_value["value"]

        return False

    def is_question_visible(self, question: BaseQuestion) -> bool:
        """
        Check if a question should be shown based on show/hide conditions.

        If a question has both show and hide conditions, show conditions are
        evaluated first (i.e. take precedence).
        """
        show_conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type="show"
        )
        hide_conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type="hide"
        )

        # If no conditions exist, the question is visible by default.
        if not show_conditions.exists() and not hide_conditions.exists():
            return True

        # Check show conditions - at least one must be met.
        if show_conditions.exists():
            show_question = self._check_conditions(show_conditions)
            return show_question

        if hide_conditions.exists():
            hide_question = self._check_conditions(hide_conditions)
            return not hide_question

        return True

    def _check_conditions(
        self, conditions: QuerySet[QuestionCondition] | QuerySet[StepCondition]
    ) -> bool:
        """Helper to evaluate whether any in a set of conditions are met."""
        for condition in conditions:
            trigger_responses = self.responses.get(condition.trigger_question.pk, [])
            if trigger_responses:
                if self.check_trigger_value(
                    trigger_responses[0].answer, condition.trigger_value
                ):
                    return True
        return False

    def get_repeat_count_for_step(self, step: Step) -> int:
        """Determine how many times a step should appear."""
        conditions = StepCondition.objects.filter(
            target_step=step, condition_type__in=["repeat", "repeat_dynamic"]
        )
        return self._get_repeat_count(conditions)

    def get_repeat_count_for_question(self, question: BaseQuestion) -> int:
        """Determine how many times a question should appear."""
        conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type__in=["repeat", "repeat_dynamic"]
        )
        return self._get_repeat_count(conditions)

    def _get_repeat_count(
        self, conditions: QuerySet[StepCondition] | QuerySet[QuestionCondition]
    ) -> int:
        """Helper to determine repeat count from conditions."""
        for condition in conditions:
            trigger_responses = self.responses.get(condition.trigger_question.pk, [])
            if not trigger_responses:
                continue

            trigger_answer = trigger_responses[0].answer

            if not self.check_trigger_value(trigger_answer, condition.trigger_value):
                continue

            if condition.use_answer_as_count:
                # Dynamic repeat based on answer value, constrained to reasonable limits.
                input_value = trigger_answer.get("value")
                return min(max(1, input_value), MAX_REPEAT_LIMIT)
            elif condition.repeat_count:
                return condition.repeat_count

        # Default: show once.
        return 1

    def is_step_visible(self, step: Step) -> bool:
        """Check if a step should be shown based on show/hide conditions."""
        show_conditions = StepCondition.objects.filter(
            target_step=step, condition_type="show"
        )
        hide_conditions = StepCondition.objects.filter(
            target_step=step, condition_type="hide"
        )

        if not show_conditions.exists() and not hide_conditions.exists():
            return True

        if show_conditions.exists():
            show_step = self._check_conditions(show_conditions)
            return show_step

        if hide_conditions.exists():
            hide_step = self._check_conditions(hide_conditions)
            return not hide_step

        return True

    def get_user_answer(
        self, question: BaseQuestion, repeat_index: int = 0
    ) -> dict | None:
        """Get the user's answer for a specific question instance."""
        responses = self.responses.get(question.pk, [])
        for response in responses:
            if response.repeat_index == repeat_index:
                return response.answer
        return None
