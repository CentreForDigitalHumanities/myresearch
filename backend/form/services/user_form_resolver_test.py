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
    UserFormSubmission,
)
from form.services.form_evaluator import FormEvaluator
from form.services.user_form_resolver import UserFormResolver


@pytest.mark.django_db
class TestUserFormResolver:
    """Tests for UserFormResolver."""

    def test_resolve_returns_user_form_type(self, form, test_user):
        """UserFormResolver.resolve() should return a UserFormType."""
        evaluator = FormEvaluator(form, test_user, create_submission=True)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        assert result.form_id == form.pk
        assert result.submission_id is not None

    def test_resolve_excludes_hidden_questions(
        self, form, test_user, trigger_question, target_question
    ):
        """Resolver should exclude questions hidden by conditions."""
        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type="show",
            trigger_value={"value": "show_me"},
        )

        # No response matching the condition
        evaluator = FormEvaluator(form, test_user, create_submission=True)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        # target_question should not be in the resolved questions
        all_questions = []
        for step in result.steps:  # type: ignore
            all_questions.extend(step.questions)

        question_ids = [q.question_id for q in all_questions]
        assert target_question.pk not in question_ids

    def test_resolve_includes_shown_questions(
        self, form, test_user, trigger_question, target_question
    ):
        """Resolver should include questions shown by conditions."""
        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type="show",
            trigger_value={"value": "show_me"},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": "show_me"},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        all_questions = []
        for step in result.steps:  # type: ignore
            all_questions.extend(step.questions)

        question_ids = [q.question_id for q in all_questions]
        assert target_question.pk in question_ids

    def test_resolve_excludes_hidden_steps(self, form, test_user):
        """Resolver should exclude steps hidden by conditions."""
        # Create two steps
        step1 = Step.objects.create(name="Step 1", slug="step-1", form=form)
        step2 = Step.objects.create(name="Step 2", slug="step-2", form=form)

        trigger_q = TextQuestion.objects.create(text="Trigger", step=step1)

        StepCondition.objects.create(
            target_step=step2,
            trigger_question=trigger_q,
            condition_type="show",
            trigger_value={"value": "show_step2"},
        )

        # No matching response
        evaluator = FormEvaluator(form, test_user, create_submission=True)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        step_ids = [s.step_id for s in result.steps]  # type: ignore
        assert step1.pk in step_ids
        assert step2.pk not in step_ids

    def test_resolve_repeats_questions(
        self, form, step, test_user, trigger_question, target_question
    ):
        """Resolver should create multiple question instances for repeat conditions."""

        NUM_OF_REPEATS = 3

        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type=BaseCondition.ConditionType.REPEAT,
            trigger_value={},
            repeat_count=NUM_OF_REPEATS,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": "trigger"},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        all_questions = []
        for step in result.steps:  # type: ignore
            all_questions.extend(step.questions)

        # Count instances of target_question
        target_instances = [
            q for q in all_questions if q.question_id == target_question.pk
        ]
        assert len(target_instances) == NUM_OF_REPEATS

        # Check repeat indices
        repeat_indices = [q.repeat_index for q in target_instances]
        assert sorted(repeat_indices) == list(range(NUM_OF_REPEATS))

    def test_resolve_repeats_steps(self, form, test_user):
        """Resolver should create multiple step instances for repeat conditions."""

        NUM_OF_REPEATS = 4

        step1 = Step.objects.create(name="Step 1", slug="step-1", form=form)
        step2 = Step.objects.create(name="Step 2", slug="step-2", form=form)

        trigger_q = NumberQuestion.objects.create(text="How many?", step=step1)

        StepCondition.objects.create(
            target_step=step2,
            trigger_question=trigger_q,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={},
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr = QuestionResponse.objects.create(
            question=trigger_q,
            answer={"value": NUM_OF_REPEATS},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        # Count instances of step2
        step2_instances = [s for s in result.steps if s.step_id == step2.pk]  # type: ignore
        assert len(step2_instances) == NUM_OF_REPEATS

        # Check slugs are modified for repeats
        slugs = [s.slug for s in step2_instances]
        assert "step-2" in slugs
        assert "step-2-1" in slugs
        assert "step-2-2" in slugs

    def test_resolve_with_no_submission(self, form, step, test_user):
        """Resolver should work without a submission."""
        TextQuestion.objects.create(text="Question 1", step=step)

        evaluator = FormEvaluator(form, test_user, create_submission=False)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        assert result.form_id == form.pk
        assert result.submission_id is None
        assert len(result.steps) > 0  # type: ignore

    def test_resolve_substeps(self, form, test_user):
        """Resolver should include substeps in the resolved form."""
        parent_step = Step.objects.create(
            name="Parent Step", slug="parent-step", form=form
        )
        substep = Step.objects.create(
            name="Substep", slug="sub-step", parent=parent_step
        )

        TextQuestion.objects.create(text="Parent Question", step=parent_step)
        TextQuestion.objects.create(text="Sub Question", step=substep)

        evaluator = FormEvaluator(form, test_user, create_submission=True)
        resolver = UserFormResolver(evaluator)

        result = resolver.resolve()

        # The parent step should have a list of substeps including sub_step
        parent_in_result = [s for s in result.steps if s.step_id == parent_step.pk][0]  # type: ignore
        assert len(parent_in_result.substeps) == 1
        assert parent_in_result.substeps[0].step_id == substep.pk


@pytest.mark.django_db
class TestComplexConditionScenarios:
    """Tests for complex condition scenarios."""

    def test_chained_show_conditions(self, form, test_user):
        """Test question shown by chained conditions."""
        step = Step.objects.create(name="Step", slug="step", form=form)

        SHOW_Q2 = "show_q2"
        SHOW_Q3 = "show_q3"

        q1 = TextQuestion.objects.create(text="Q1", step=step)
        q2 = TextQuestion.objects.create(text="Q2", step=step)
        q3 = TextQuestion.objects.create(text="Q3", step=step)

        # Q2 depends on Q1
        QuestionCondition.objects.create(
            target_question=q2,
            trigger_question=q1,
            condition_type="show",
            trigger_value={"value": SHOW_Q2},
        )

        # Q3 depends on Q2
        QuestionCondition.objects.create(
            target_question=q3,
            trigger_question=q2,
            condition_type="show",
            trigger_value={"value": SHOW_Q3},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr1 = QuestionResponse.objects.create(question=q1, answer={"value": SHOW_Q2})
        qr1.submissions.add(submission)
        qr2 = QuestionResponse.objects.create(question=q2, answer={"value": SHOW_Q3})
        qr2.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        assert evaluator.is_question_visible(q1) is True
        assert evaluator.is_question_visible(q2) is True
        assert evaluator.is_question_visible(q3) is True

    def test_show_and_hide_conditions_show_wins(self, form, test_user):
        """When both show and hide conditions are met, show should take precedence."""
        SHOW_VALUE = "show"
        HIDE_VALUE = "hide"

        step = Step.objects.create(name="Step", slug="step", form=form)

        trigger_show = TextQuestion.objects.create(text="Show Trigger", step=step)
        trigger_hide = TextQuestion.objects.create(text="Hide Trigger", step=step)
        target = TextQuestion.objects.create(text="Target", step=step)

        QuestionCondition.objects.create(
            target_question=target,
            trigger_question=trigger_show,
            condition_type="show",
            trigger_value={"value": SHOW_VALUE},
        )

        QuestionCondition.objects.create(
            target_question=target,
            trigger_question=trigger_hide,
            condition_type="hide",
            trigger_value={"value": HIDE_VALUE},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)
        qr1 = QuestionResponse.objects.create(
            question=trigger_show, answer={"value": SHOW_VALUE}
        )
        qr1.submissions.add(submission)
        qr2 = QuestionResponse.objects.create(
            question=trigger_hide, answer={"value": HIDE_VALUE}
        )
        qr2.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        # Show conditions take precedence over hide, so if both are met, the
        # question should be visible.
        assert evaluator.is_question_visible(target) is True

    def test_multiple_select_options_any_match(self, form, test_user):
        """Condition should trigger if any of multiple select options match."""
        step = Step.objects.create(name="Step", slug="step", form=form)

        select_question = SelectQuestion.objects.create(
            text="Select", step=step, multiple=True
        )
        option_1 = SelectOption.objects.create(
            label="Option 1",
            question=select_question,
        )
        option_2 = SelectOption.objects.create(
            label="Option 2",
            question=select_question,
        )
        option_3 = SelectOption.objects.create(
            label="Option 3",
            question=select_question,
        )

        target = TextQuestion.objects.create(text="Target", step=step)

        # Trigger on option_1 or option_2
        QuestionCondition.objects.create(
            target_question=target,
            trigger_question=select_question,
            condition_type="show",
            trigger_value={"value": [option_1.pk, option_2.pk]},
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)

        # User selects option 3 only.
        qr = QuestionResponse.objects.create(
            question=select_question,
            answer={"value": [option_3.pk]},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)
        assert evaluator.is_question_visible(target) is False

        # All options in the condition are selected.
        QuestionResponse.objects.filter(question=select_question).update(
            answer={"value": [option_1.pk, option_2.pk]}
        )
        evaluator._responses_cache = None  # Clear cache

        assert evaluator.is_question_visible(target) is True

        # User selects all options.
        QuestionResponse.objects.filter(question=select_question).update(
            answer={"value": [option_1.pk, option_2.pk, option_3.pk]}
        )
        evaluator._responses_cache = None  # Clear cache

        assert evaluator.is_question_visible(target) is True

    def test_repeat_with_conditional_trigger_value(self, form, test_user):
        """Repeat condition should only trigger when trigger_value matches."""

        MINIMAL_VALUE = 2

        step = Step.objects.create(name="Step", slug="step", form=form)

        trigger_question = NumberQuestion.objects.create(text="How many?", step=step)
        target_question = TextQuestion.objects.create(text="Repeated Q", step=step)

        # Only repeat if answer >= 2
        QuestionCondition.objects.create(
            target_question=target_question,
            trigger_question=trigger_question,
            condition_type=BaseCondition.ConditionType.REPEAT_DYNAMIC,
            trigger_value={"min": MINIMAL_VALUE},
            use_answer_as_count=True,
        )

        submission = UserFormSubmission.objects.create(user=test_user, form=form)

        # Answer does not meet condition.
        qr = QuestionResponse.objects.create(
            question=trigger_question,
            answer={"value": MINIMAL_VALUE - 1},
        )
        qr.submissions.add(submission)

        evaluator = FormEvaluator(form, test_user)

        # Should default to 1, as the condition is not met.
        assert evaluator.get_repeat_count_for_question(target_question) == 1

        # Update answer to MINIMAL_VALUE + 1.
        QuestionResponse.objects.filter(question=trigger_question).update(
            answer={"value": MINIMAL_VALUE + 1}
        )
        evaluator._responses_cache = None  # Clear cache

        # Now the question should repeat MINIMAL_VALUE + 1 times.
        assert (
            evaluator.get_repeat_count_for_question(target_question)
            == MINIMAL_VALUE + 1
        )
