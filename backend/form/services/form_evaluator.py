from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from form.models import (
    BaseCondition,
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

# How often we will allow a question or step to be repeated.
MAX_REPEAT_LIMIT = 10


class FormEvaluator:
    """
    Creates a user-specific view of a form, with conditional logic and repeats
    applied, based on a user's submission.

    Args:
        submission: The submission to be evaluated.
    """

    def __init__(self, submission: UserFormSubmission):
        self.submission = submission
        self._responses_cache = None

    @property
    def form(self) -> MRForm:
        """Get the form associated with this submission."""
        return self.submission.form

    @property
    def responses(self) -> dict[int, list[QuestionResponse]]:
        """Cache all responses for this submission, grouped by question_id."""
        if self._responses_cache is None:
            self._responses_cache = {}
            if self.submission:
                responses = QuestionResponse.objects.filter(
                    submissions=self.submission
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

        # Use a less cumbersome alias.
        VK = BaseCondition.TriggerValueKeys

        # Number comparisons
        if VK.MIN in trigger_value:
            return answer.get("value", 0) >= trigger_value[VK.MIN]
        if VK.MAX in trigger_value:
            return answer.get("value", 0) <= trigger_value[VK.MAX]
        if VK.EXACT in trigger_value:
            return answer.get("value") == trigger_value[VK.EXACT]

        # Direct value match (for booleans, strings, etc.)
        if VK.VALUE in trigger_value:
            match_value = trigger_value[VK.VALUE]
            user_answer = answer.get("value")

            # Convert to strings for comparison
            match_value_str = str(match_value)
            if user_answer is None:
                return False
            user_answer_str = str(user_answer)

            match_value_list = [v.strip() for v in match_value_str.split(",")]
            user_answer_list = [v.strip() for v in user_answer_str.split(",")]

            return all(val in user_answer_list for val in match_value_list)

        return False

    def is_question_visible(self, question: BaseQuestion) -> bool:
        """
        Check if a question should be shown based on show/hide conditions.

        If a question has both show and hide conditions, show conditions are
        evaluated first (i.e. take precedence).
        """
        show_conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type=BaseCondition.ConditionType.SHOW
        )
        hide_conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type=BaseCondition.ConditionType.HIDE
        )

        # If no conditions exist, the question is visible by default.
        if not show_conditions.exists() and not hide_conditions.exists():
            return True

        # Check show conditions - at least one must be met.
        if show_conditions.exists():
            return any(
                self._condition_is_met(condition) for condition in show_conditions
            )

        if hide_conditions.exists():
            return not any(
                self._condition_is_met(condition) for condition in hide_conditions
            )

        return True

    def _condition_is_met(self, condition: QuestionCondition | StepCondition) -> bool:
        """
        Helper to evaluate whether a condition is met.

        Returns True if *any* response to the trigger question matches the trigger value.
        """
        trigger_responses = self.responses.get(condition.trigger_question.pk, [])
        # Returns False if list is empty.
        return any(
            self.check_trigger_value(response.answer, condition.trigger_value)
            for response in trigger_responses
        )

    def get_repeat_count_for_step(self, step: Step) -> int:
        """Determine how many times a step should appear."""
        conditions = StepCondition.objects.filter(
            target_step=step,
            condition_type__in={
                BaseCondition.ConditionType.REPEAT,
                BaseCondition.ConditionType.REPEAT_DYNAMIC,
            },
        )
        return self._get_repeat_count(conditions)

    def get_repeat_count_for_question(self, question: BaseQuestion) -> int:
        """Determine how many times a question should appear."""
        conditions = QuestionCondition.objects.filter(
            target_question=question,
            condition_type__in={
                BaseCondition.ConditionType.REPEAT,
                BaseCondition.ConditionType.REPEAT_DYNAMIC,
            },
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
                return min(max(0, input_value), MAX_REPEAT_LIMIT)
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

        # Check show conditions - at least one must be met.
        if show_conditions.exists():
            return any(
                self._condition_is_met(condition) for condition in show_conditions
            )

        if hide_conditions.exists():
            return not any(
                self._condition_is_met(condition) for condition in hide_conditions
            )

        return True

    def get_user_response(
        self,
        question: BaseQuestion,
        repeat_index=None,
    ) -> QuestionResponse | None:
        """Get the user's response for a specific question instance."""
        responses = self.responses.get(question.pk, [])
        for response in responses:
            if response.repeat_index == repeat_index:
                # Normally, responses to the same question with both
                # repeat_index=None and repeat_index=not_None should
                # never coexist. So this check should be considered
                # for removal when the repeat_index argument to this
                # method is None.
                return response
        return None
