import pytest

from form.models import (
    BaseCondition,
    NumberQuestion,
    QuestionCondition,
    QuestionResponse,
    SelectOption,
    SelectQuestion,
    Step,
    StepCondition,
    TextQuestion,
    TrueFalseQuestion,
    UserFormSubmission,
)
from form.services.form_evaluator import MAX_REPEAT_LIMIT, FormEvaluator


@pytest.mark.django_db
class TestFormEvaluatorCheckTriggerValue:
    """Tests for FormEvaluator.check_trigger_value method."""

    def test_empty_trigger_value_returns_true_for_any_answer(self, form, test_user):
        """Empty trigger_value dict should match any non-empty answer."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({"value": "anything"}, {}) is True
        assert evaluator.check_trigger_value({"value": 123}, {}) is True
        assert evaluator.check_trigger_value({"value": True}, {}) is True

    def test_empty_trigger_value_returns_false_for_empty_answer(self, form, test_user):
        """Empty trigger_value dict should match any answer, including empty/falsy ones."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({}, {}) is True
        assert evaluator.check_trigger_value({"value": ""}, {}) is True
        assert evaluator.check_trigger_value({"value": 0}, {}) is True

    def test_min_comparison(self, form, test_user):
        """Test minimum value comparison."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({"value": 10}, {"min": 5}) is True
        assert evaluator.check_trigger_value({"value": 5}, {"min": 5}) is True
        assert evaluator.check_trigger_value({"value": 3}, {"min": 5}) is False

    def test_max_comparison(self, form, test_user):
        """Test maximum value comparison."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({"value": 3}, {"max": 5}) is True
        assert evaluator.check_trigger_value({"value": 5}, {"max": 5}) is True
        assert evaluator.check_trigger_value({"value": 10}, {"max": 5}) is False

    def test_exact_comparison(self, form, test_user):
        """Test exact value comparison."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({"value": 5}, {"exact": 5}) is True
        assert evaluator.check_trigger_value({"value": 10}, {"exact": 5}) is False
        assert (
            evaluator.check_trigger_value({"value": "hello"}, {"exact": "hello"})
            is True
        )

    def test_value_matching_with_single_option(self, form, test_user):
        """Test value matching with single select."""
        evaluator = FormEvaluator(form, test_user)

        assert (
            evaluator.check_trigger_value(
                answer={"value": [1]},
                trigger_value={"value": [1]},
            )
            is True
        )
        assert (
            evaluator.check_trigger_value(
                answer={"value": [5]},
                trigger_value={"value": [1]},
            )
            is False
        )

    def test_value_matching_with_multiple_options(self, form, test_user):
        """Test value matching with multiple select."""
        evaluator = FormEvaluator(form, test_user)

        # Complete match
        assert (
            evaluator.check_trigger_value(
                answer={"value": [1, 2, 3]},
                trigger_value={"value": [1, 2, 3]},
            )
            is True
        )

        # Answer has extra value: condition is met.
        assert (
            evaluator.check_trigger_value(
                answer={"value": [1, 2, 3]},
                trigger_value={"value": [1, 2]},
            )
            is True
        )

        # Answer lacks one value: condition is not met.
        assert (
            evaluator.check_trigger_value(
                answer={"value": [1, 2]},
                trigger_value={"value": [1, 2, 3]},
            )
            is False
        )

    def test_value_comparison_for_booleans(self, form, test_user):
        """Test direct value matching for booleans."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({"value": True}, {"value": True}) is True
        assert evaluator.check_trigger_value({"value": False}, {"value": True}) is False
        assert evaluator.check_trigger_value({"value": False}, {"value": False}) is True

    def test_value_comparison_for_strings(self, form, test_user):
        """Test direct value matching for strings."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.check_trigger_value({"value": "yes"}, {"value": "yes"}) is True
        assert evaluator.check_trigger_value({"value": "no"}, {"value": "yes"}) is False


@pytest.mark.django_db
class TestFormEvaluatorQuestionConditions:
    """Tests for QuestionCondition evaluation in FormEvaluator."""

    def test_question_visible_by_default_without_conditions(
        self, form, test_user, target_question
    ):
        """Question without conditions should be visible by default."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(target_question) is True

    def test_show_condition_hides_question_when_not_met(
        self, form, test_user, trigger_question, target_question
    ):
        """Question with show condition should be hidden when condition is not met."""
        # Create show condition
        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type="show",
            trigger_value={"value": "specific_answer"},
        )

        evaluator = FormEvaluator(form, test_user)

        # No submission/response means condition not met
        assert evaluator.is_question_visible(target_question) is False

    def test_show_condition_shows_question_when_met(
        self, form, test_user, trigger_question, target_question
    ):
        """Question with show condition should be visible when condition is met."""

        SPECIFIC_ANSWER = "specific_answer"

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type="show",
            trigger_value={"value": SPECIFIC_ANSWER},
        )

        # Create submission and response
        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": SPECIFIC_ANSWER},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(target_question) is True

    def test_hide_condition_shows_question_when_not_met(
        self, form, test_user, trigger_question, target_question
    ):
        """Question with hide condition should be visible when condition is not met."""
        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type="hide",
            trigger_value={"value": "hide_me"},
        )

        evaluator = FormEvaluator(form, test_user)

        # No response means the hide condition is not met, so question is shown.
        assert evaluator.is_question_visible(target_question) is True

    def test_hide_condition_hides_question_when_met(
        self, form, test_user, trigger_question, target_question
    ):
        """Question with hide condition should be hidden when condition is met."""
        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type="hide",
            trigger_value={"value": "hide_me"},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": "hide_me"},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(target_question) is False

    def test_show_condition_with_boolean_trigger(
        self, form, step, test_user, target_question
    ):
        """Show condition triggered by boolean (TrueFalse) question."""
        bool_trigger = TrueFalseQuestion.objects.create(
            text="Do you want more?",
            step=step,
        )

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=bool_trigger,
            condition_type="show",
            trigger_value={"value": True},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=bool_trigger,
            answer={"value": True},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(target_question) is True

    def test_show_condition_with_select_option_trigger(
        self, form, step, test_user, target_question
    ):
        """Show condition triggered by select option."""
        select_trigger = SelectQuestion.objects.create(
            text="Choose an option",
            step=step,
            multiple=False,
        )
        option1 = SelectOption.objects.create(label="Option 1", question=select_trigger)
        option2 = SelectOption.objects.create(label="Option 2", question=select_trigger)

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=select_trigger,
            condition_type="show",
            trigger_value={"value": [option1.pk, option2.pk]},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=select_trigger,
            answer={"value": [option1.pk, option2.pk]},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(target_question) is True

    def test_show_condition_with_number_min_trigger(
        self, form, step, test_user, target_question
    ):
        """Show condition triggered by number >= min value."""
        number_trigger = NumberQuestion.objects.create(
            text="How many?",
            step=step,
        )

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=number_trigger,
            condition_type="show",
            trigger_value={"min": 5},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=number_trigger,
            answer={"value": 7},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(target_question) is True

    def test_repeat_condition_static_count(
        self, form, test_user, trigger_question, target_question
    ):
        """Question with repeat condition should return static repeat count."""

        NUMBER_OF_REPEATS = 3

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type=BaseCondition.ConditionType.REPEAT,
            trigger_value={},  # Any answer triggers
            repeat_count=NUMBER_OF_REPEATS,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": "anything"},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert (
            evaluator.get_repeat_count_for_question(target_question)
            == NUMBER_OF_REPEATS
        )

    def test_repeat_dynamic_condition_uses_answer_value(
        self, form, step, test_user, target_question
    ):
        """Question with repeat_dynamic should use answer value as count."""

        NUMBER_OF_REPEATS = 5

        number_trigger = NumberQuestion.objects.create(
            text="How many times?",
            step=step,
        )

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=number_trigger,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={},  # Any answer triggers
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=number_trigger,
            answer={"value": NUMBER_OF_REPEATS},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert (
            evaluator.get_repeat_count_for_question(target_question)
            == NUMBER_OF_REPEATS
        )

    def test_repeat_dynamic_minimum_is_one(
        self, form, step, test_user, target_question
    ):
        """Repeat count should be at least 1 even with 0 or negative answer."""
        number_trigger = NumberQuestion.objects.create(
            text="How many times?",
            step=step,
        )

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=number_trigger,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={},
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=number_trigger,
            answer={"value": 0},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_question(target_question) == 1

    def test_no_repeat_condition_returns_one(self, form, test_user, target_question):
        """Question without repeat condition should have repeat count of 1."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_question(target_question) == 1


@pytest.mark.django_db
class TestFormEvaluatorStepConditions:
    """Tests for StepCondition evaluation in FormEvaluator."""

    def test_step_visible_by_default_without_conditions(self, form, step, test_user):
        """Step without conditions should be visible by default."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_step_visible(step) is True

    def test_show_condition_hides_step_when_not_met(
        self, form, step, test_user, trigger_question
    ):
        """Step with show condition should be hidden when condition is not met."""
        StepCondition.objects.create(
            target_step=step,
            trigger_question=trigger_question,
            condition_type="show",
            trigger_value={"value": "show_step"},
        )

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_step_visible(step) is False

    def test_show_condition_shows_step_when_met(
        self, form, step, test_user, trigger_question
    ):
        """Step with show condition should be visible when condition is met."""
        # Create another step to hold the trigger question.
        trigger_step = Step.objects.create(
            name="Trigger Step", slug="trigger-step", form=form
        )
        trigger_q = TextQuestion.objects.create(text="Trigger", step=trigger_step)

        SPECIFIC_ANSWER = "show_step"

        StepCondition.objects.create(
            target_step=step,
            trigger_question=trigger_q,
            condition_type="show",
            trigger_value={"value": SPECIFIC_ANSWER},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_q,
            answer={"value": SPECIFIC_ANSWER},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_step_visible(step) is True

    def test_hide_condition_shows_step_when_not_met(
        self, form, step, test_user, trigger_question
    ):
        """Step with hide condition should be visible when condition is not met."""
        StepCondition.objects.create(
            target_step=step,
            trigger_question=trigger_question,
            condition_type="hide",
            trigger_value={"value": "hide_step"},
        )

        evaluator = FormEvaluator(form, test_user)

        # No response: hide condition is not met, so the step is visible.
        assert evaluator.is_step_visible(step) is True

    def test_hide_condition_hides_step_when_met(
        self, form, step, test_user, trigger_question
    ):
        """Step with hide condition should be hidden when condition is met."""

        SPECIFIC_ANSWER = "hide_step"

        StepCondition.objects.create(
            target_step=step,
            trigger_question=trigger_question,
            condition_type="hide",
            trigger_value={"value": SPECIFIC_ANSWER},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": SPECIFIC_ANSWER},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_step_visible(step) is False

    def test_step_repeat_condition_static_count(
        self, form, step, test_user, trigger_question
    ):
        """Step with repeat condition should return static repeat count."""

        REPEAT_COUNT = 4

        StepCondition.objects.create(
            target_step=step,
            trigger_question=trigger_question,
            condition_type=BaseCondition.ConditionType.REPEAT,
            trigger_value={},
            repeat_count=REPEAT_COUNT,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": "trigger"},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_step(step) == REPEAT_COUNT

    def test_step_repeat_dynamic_uses_answer_value(self, form, step, test_user):
        """Step with repeat_dynamic should use answer value as count."""
        number_trigger = NumberQuestion.objects.create(
            text="How many steps?",
            step=step,
        )

        REPEAT_COUNT = 3

        StepCondition.objects.create(
            target_step=step,
            trigger_question=number_trigger,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={},
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=number_trigger,
            answer={"value": REPEAT_COUNT},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_step(step) == REPEAT_COUNT

    def test_step_repeat_dynamic_minimum_is_one(self, form, step, test_user):
        """Step repeat count should be at least 1."""
        number_trigger = NumberQuestion.objects.create(
            text="How many steps?",
            step=step,
        )

        StepCondition.objects.create(
            target_step=step,
            trigger_question=number_trigger,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={},
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=number_trigger,
            answer={"value": -5},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_step(step) == 1

    def test_step_repeate_dynamic_maximum_limit(self, form, step, test_user):
        """Step repeat count should not exceed maximum limit."""
        number_trigger = NumberQuestion.objects.create(
            text="How many steps?",
            step=step,
        )

        EXCESSIVE_COUNT = 99999999999

        StepCondition.objects.create(
            target_step=step,
            trigger_question=number_trigger,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={},
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=number_trigger,
            answer={"value": EXCESSIVE_COUNT},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_step(step) == MAX_REPEAT_LIMIT

    def test_no_step_repeat_condition_returns_one(self, form, step, test_user):
        """Step without repeat condition should have repeat count of 1."""
        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_repeat_count_for_step(step) == 1


@pytest.mark.django_db
class TestFormEvaluatorSubmission:
    """Tests for FormEvaluator submission handling."""

    def test_creates_submission_when_flag_set(self, form, test_user):
        """FormEvaluator should create submission when create_submission=True."""
        evaluator = FormEvaluator(form, test_user, create_submission=True)

        submission = evaluator.submission

        assert submission is not None
        assert submission.user == test_user
        assert submission.form == form

    def test_returns_none_when_no_submission_exists(self, form, test_user):
        """FormEvaluator should return None when no submission exists."""
        evaluator = FormEvaluator(form, test_user, create_submission=False)

        assert evaluator.submission is None

    def test_returns_latest_submission(self, form, test_user):
        """FormEvaluator should return the most recent submission."""
        # Create older submission
        UserFormSubmission.objects.create(user=test_user, form=form)
        # Create newer submission
        newer = UserFormSubmission.objects.create(user=test_user, form=form)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.submission == newer

    def test_get_user_answer(self, form, test_user, trigger_question):
        """Test get_user_answer retrieves correct answer."""
        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": "my answer"},
            repeat_index=0,
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        response = evaluator.get_user_response(trigger_question, 0)
        assert response is not None
        assert response.answer == {"value": "my answer"}
        assert evaluator.get_user_response(trigger_question, 1) is None

    def test_get_user_answer_with_repeat_index(self, form, test_user, trigger_question):
        """Test get_user_answer with different repeat indices."""

        FIRST_ANSWER = "first"
        SECOND_ANSWER = "second"

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": FIRST_ANSWER},
            repeat_index=0,
        )
        qr.submissions.add(submission)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": SECOND_ANSWER},
            repeat_index=1,
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.get_user_response(trigger_question, 0).answer == {
            "value": FIRST_ANSWER
        }
        assert evaluator.get_user_response(trigger_question, 1).answer == {
            "value": SECOND_ANSWER
        }
