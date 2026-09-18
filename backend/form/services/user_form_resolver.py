from graphene import ObjectType

from form.models import BaseQuestion, Step, RepeatIndex
from form.models.questions import RepeatableStepQuestion
from form.services.form_evaluator import FormEvaluator
from form.types.StepType import StepType
from form.types.UserFormType import UserFormType
from form.types.QuestionType import (
    DateQuestionType,
    FileUploadQuestionType,
    NumberQuestionType,
    SelectQuestionType,
    TextQuestionType,
    TrueFalseQuestionType,
    RepeatableStepQuestionType,
)


class UserFormResolver:
    """
    Transforms the user-specific form (evaluated with FormEvaluator) into GraphQL types.
    """

    def __init__(self, evaluator: FormEvaluator):
        self.evaluator = evaluator

    def resolve(self) -> UserFormType:
        """Resolve the complete user form structure."""
        form = self.evaluator.form
        submission = self.evaluator.submission

        steps = self._resolve_steps()

        return UserFormType(
            form_id=form.pk,  # type: ignore
            name_nl=form.name_nl,  # type: ignore
            name_en=form.name_en,  # type: ignore
            steps=steps,  # type: ignore
            submission_id=submission.pk if submission else None,  # type: ignore
            started_at=submission.started_at if submission else None,  # type: ignore
            completed_at=submission.completed_at if submission else None,  # type: ignore
        )

    def _resolve_steps(
        self,
        parent_step: Step | None = None,
        parent_index: RepeatIndex | None = None,
    ) -> list[StepType]:

        form = self.evaluator.submission.form

        if not parent_step:
            steps = Step.objects.filter(form=form, parent__isnull=True).all()
        else:
            steps = Step.objects.filter(parent=parent_step).all()

        instances: list[StepType] = []
        for step in steps:
            # Skip hidden steps
            if not self.evaluator.is_step_visible(step):
                continue
            # Check for repeatability
            if step.is_repeatable:
                instances.extend(
                    self._resolve_step_repeats(
                        step,
                        parent_index=parent_index,
                    ),
                )
            else:
                instances.append(
                    self._create_step_instance(
                        step,
                        repeat_index=parent_index,
                    )
                )
        return instances

    def _resolve_step_repeats(
        self, step: Step, parent_index: RepeatIndex | None = None
    ) -> list[StepType]:
        repeated_steps: list[StepType] = []

        repeat_indices = step.repeat_indices_for_submission(
            submission=self.evaluator.submission,
            parent_index=parent_index,
        )
        for index in repeat_indices:
            # Now we construct the step instances that will actually appear
            # because there are repeat indices for this step linked
            # to this submission.
            instance = self._create_step_instance(
                step,
                repeat_index=index,
            )
            repeated_steps.append(instance)
        return repeated_steps

    def _create_step_instance(
        self, step: Step, repeat_index: RepeatIndex | None = None
    ) -> StepType:
        questions, step_name_override = self._resolve_step_questions(step, repeat_index)
        substeps = self._resolve_steps(
            parent_step=step,
            parent_index=repeat_index,
        )

        slug = generate_slug(step, repeat_index=repeat_index)

        if repeat_index is not None:
            repeat_index = repeat_index.pk

        return StepType(
            step_id=step.pk,  # type: ignore
            name_nl=step_name_override if step_name_override else step.name_nl,  # type: ignore
            name_en=step_name_override if step_name_override else step.name_en,  # type: ignore
            description_nl=step.description_nl,  # type: ignore
            description_en=step.description_en,  # type: ignore
            slug=slug,
            repeat_index=repeat_index,  # type: ignore
            is_overview=step.is_overview,  # type: ignore
            questions=questions,  # type: ignore
            substeps=substeps,  # type: ignore
        )

    def _resolve_step_questions(
        self, step: Step, repeat_index: RepeatIndex | None = None
    ):
        # TODO: make question instances from step, rather than questions
        # Check out the old implementation
        questions = []
        step_name_override = False
        step_questions = list(BaseQuestion.objects.filter(step=step))
        for question in step_questions:
            # Skip hidden questions
            if not self.evaluator.is_question_visible(question):
                continue
            resolved_questions = self._resolve_question_instances(
                question,
                repeat_index,
            )
            # We assume that a step_name_override question is never
            # repeatable, so we work with the first in the list.
            if question.step_name_override:
                try:
                    answer = resolved_questions[0].answer
                except IndexError:
                    # This should never happen, as we always expect at least one question
                    continue
                if answer:
                    step_name_override = answer["value"]
            questions.extend(resolved_questions)
        return questions, step_name_override

    def _resolve_question_instances(
        self, question: BaseQuestion, repeat_index: RepeatIndex | None
    ) -> list:
        """Resolve all instances of a question (considering repeats).
        Also deletes hidden responses as a side effect."""

        question = question.get_subclass()

        if question.is_repeatable:
            return self._resolve_question_repeats(
                question,
                parent_index=repeat_index,
            )
        # When this question isn't repeatable, just return a single instance.
        instance = self._create_question_instance(
            question,
            repeat_index,
        )

        return [instance]

    def _resolve_question_repeats(
        self,
        question: BaseQuestion,
        parent_index: RepeatIndex | None = None,
    ):
        repeats = []

        repeat_indices = question.repeat_indices_for_submission(
            submission=self.evaluator.submission,
            parent_index=parent_index,
        )

        # For repeatable questions, we'll always want at least one repeat.
        if not repeat_indices:
            new_repeat = RepeatIndex(
                parent=parent_index,
            )
            new_repeat.save()
            new_repeat.submissions.add(self.evaluator.submission)
            question.repeat_indices.add(new_repeat)

        for index in repeat_indices:
            # Now we construct the step instances that will actually appear
            # because there are repeat indices for this question linked
            # to this submission.
            instance = self._create_question_instance(
                question,
                repeat_index=index,
                repeatable=True,
            )
            repeats.append(instance)
        return repeats

    def _create_question_instance(
        self,
        question: BaseQuestion,
        repeat_index: RepeatIndex | None = None,
        repeatable=False,
    ) -> ObjectType:
        """Create the appropriate user question instance type based on the question type."""

        response = self.evaluator.get_user_response(question, repeat_index)

        base_data = {
            "question_id": question.pk,
            "repeat_index": repeat_index.pk if repeat_index else None,
            "answer": response.answer if response else None,
            "response_id": response.pk if response else None,
            # The 'question' field is used for BaseQuestionInterface.resolve_type.
            "question": question,
            "is_repeatable": repeatable,
        }

        # Access the specific subclass using Django's reverse relation attributes
        if hasattr(question, "textquestion"):
            return TextQuestionType(**base_data)
        elif hasattr(question, "numberquestion"):
            return NumberQuestionType(**base_data)
        elif hasattr(question, "truefalsequestion"):
            return TrueFalseQuestionType(**base_data)
        elif hasattr(question, "datequestion"):
            return DateQuestionType(**base_data)
        elif hasattr(question, "selectquestion"):
            return SelectQuestionType(**base_data)
        elif hasattr(question, "fileuploadquestion"):
            return FileUploadQuestionType(**base_data)
        elif hasattr(question, "repeatablestepquestion"):
            assert isinstance(question, RepeatableStepQuestion)
            base_data["answer"] = question.get_answer(
                parent_index=repeat_index,
                submission=self.evaluator.submission,
            )
            return RepeatableStepQuestionType(**base_data)

        # Fallback (should not happen)
        return TextQuestionType(**base_data)


# TODO: Move these helpers somewhere else
def generate_slug(
    sluggable,
    repeat_index: RepeatIndex | None = None,
):
    """
    Generate a slug for a stop or question that is unique within a
    submission. Can be used to reference or link to the items on a page.
    """
    slug = getattr(sluggable, "slug", sluggable.id)
    parts = [slug]
    if repeat_index is not None:
        parts.append(str(repeat_index.pk))
    return ".".join(parts)

