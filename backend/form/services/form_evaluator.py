from typing import Dict, List, Tuple, Optional
from django.contrib.auth import get_user_model

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


class FormEvaluator:
    """Evaluates conditional logic to determine visible questions/steps for a user."""

    def __init__(self, form: MRForm, user: UserType):
        self.form = form
        self.user = user
        self._submission = None
        self._responses_cache = None

    @property
    def submission(self) -> Optional[UserFormSubmission]:
        """Get or create the user's submission."""
        if self._submission is None:
            self._submission, _ = UserFormSubmission.objects.get_or_create(
                user=self.user, form=self.form
            )
        return self._submission

    @property
    def responses(self) -> Dict[int, List[QuestionResponse]]:
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

    def check_trigger_value(self, answer: Dict, trigger_value: Dict) -> bool:
        """Check if an answer matches the trigger condition."""
        if not trigger_value:  # Empty dict = any answer
            return bool(answer)

        # Number comparisons
        if "min" in trigger_value:
            return answer.get("value", 0) >= trigger_value["min"]
        if "max" in trigger_value:
            return answer.get("value", 0) <= trigger_value["max"]
        if "exact" in trigger_value:
            return answer.get("value") == trigger_value["exact"]

        # Select option checks
        if "option_ids" in trigger_value:
            user_option_ids = answer.get("option_ids", [])
            if "option_id" in answer:
                user_option_ids = [answer["option_id"]]
            return any(opt in trigger_value["option_ids"] for opt in user_option_ids)

        # Direct value match (for booleans, strings, etc.)
        if "value" in trigger_value:
            return answer.get("value") == trigger_value["value"]

        return False

    def get_repeat_count_for_question(self, question: BaseQuestion) -> int:
        """Determine how many times a question should appear."""
        conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type__in=["repeat", "repeat_dynamic"]
        )

        for condition in conditions:
            trigger_responses = self.responses.get(condition.trigger_question.pk, [])
            if not trigger_responses:
                continue

            # Use the first response (repeat_index=0) as the trigger
            trigger_answer = trigger_responses[0].answer

            if not self.check_trigger_value(trigger_answer, condition.trigger_value):
                continue

            if condition.use_answer_as_count:
                # Dynamic repeat based on answer value
                return max(1, trigger_answer.get("value", 1))
            elif condition.repeat_count:
                # Static repeat count
                return condition.repeat_count

        return 1  # Default: show once

    def is_question_visible(self, question: BaseQuestion) -> bool:
        """Check if a question should be shown based on show/hide conditions."""
        show_conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type="show"
        )
        hide_conditions = QuestionCondition.objects.filter(
            target_question=question, condition_type="hide"
        )

        # If no conditions, it's visible by default
        if not show_conditions.exists() and not hide_conditions.exists():
            return True

        # Check show conditions - at least one must be met
        if show_conditions.exists():
            show_condition_met = False
            for condition in show_conditions:
                trigger_responses = self.responses.get(
                    condition.trigger_question.pk, []
                )
                if trigger_responses:
                    if self.check_trigger_value(
                        trigger_responses[0].answer, condition.trigger_value
                    ):
                        show_condition_met = True
                        break
            if not show_condition_met:
                return False

        # Check hide conditions - if any is met, hide the question
        for condition in hide_conditions:
            trigger_responses = self.responses.get(condition.trigger_question.pk, [])
            if trigger_responses:
                if self.check_trigger_value(
                    trigger_responses[0].answer, condition.trigger_value
                ):
                    return False

        return True

    def get_repeat_count_for_step(self, step: Step) -> int:
        """Determine how many times a step should appear."""
        conditions = StepCondition.objects.filter(
            target_step=step, condition_type__in=["repeat", "repeat_dynamic"]
        )

        for condition in conditions:
            trigger_responses = self.responses.get(condition.trigger_question.pk, [])
            if not trigger_responses:
                continue

            trigger_answer = trigger_responses[0].answer

            if not self.check_trigger_value(trigger_answer, condition.trigger_value):
                continue

            if condition.use_answer_as_count:
                return max(1, trigger_answer.get("value", 1))
            elif condition.repeat_count:
                return condition.repeat_count

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
            show_condition_met = False
            for condition in show_conditions:
                trigger_responses = self.responses.get(
                    condition.trigger_question.pk, []
                )
                if trigger_responses:
                    if self.check_trigger_value(
                        trigger_responses[0].answer, condition.trigger_value
                    ):
                        show_condition_met = True
                        break
            if not show_condition_met:
                return False

        for condition in hide_conditions:
            trigger_responses = self.responses.get(condition.trigger_question.pk, [])
            if trigger_responses:
                if self.check_trigger_value(
                    trigger_responses[0].answer, condition.trigger_value
                ):
                    return False

        return True

    def get_user_answer(
        self, question: BaseQuestion, repeat_index: int = 0
    ) -> Optional[Dict]:
        """Get the user's answer for a specific question instance."""
        responses = self.responses.get(question.pk, [])
        for response in responses:
            if response.repeat_index == repeat_index:
                return response.answer
        return None
