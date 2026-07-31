from graphene import ObjectType
from typing import Optional

from form.models import BaseQuestion, Step, Repeatable
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
        parent_step: Optional[Step] = None,
        parent_index=None,
    ):

        form = self.evaluator.submission.form

        if not parent_step:
            steps = Step.objects.filter(form=form, parent__isnull=True).all()
        else:
            steps = Step.objects.filter(parent=parent_step).all()

        instances = []
        for step in steps:
            # Skip hidden steps
            if not self.evaluator.is_step_visible(step):
                continue
            # Check for repeatability
            if is_repeatable(step):
                instances.extend(
                    self._make_step_repeats(
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

    def _make_step_repeats(
        self,
        step: Step,
        parent_index=None,
    ):
        repeats = []
        # For repeatable steps, we first insert the "blank" background
        # step into the output.
        background_step = self._create_step_instance(
            step,
            repeat_index=parent_index,
            background=True,
        )
        repeats.append(background_step)
        # Then we continue by finding the step's
        # repeat_indices that correspond to this submission.
        repeat_indices = self._fetch_repeat_indices(
            step,
            parent_index=parent_index,
        )
        for index in repeat_indices:
            # Now we construct the step instances that will actually appear
            # because there are repeat indices for this question linked
            # to this submission.
            instance = self._create_step_instance(
                step,
                repeat_index=index,
            )
            repeats.append(instance)
        return repeats

    def _create_step_instance(
        self,
        step,
        repeat_index=None,
        background=False,
    ):

        if background is True:
            # Background steps for now only serve as a reference that
            # "something may exist here", so we don't need to bother the
            # frontend with their substeps or questions
            questions = []
            substeps = []
        else:
            questions = self._make_question_instances(step, repeat_index)
            substeps = self._resolve_steps(
                parent_step=step,
                parent_index=repeat_index,
            )

        slug = step.slug
        slug = generate_slug(step, repeat_index=repeat_index)

        if repeat_index is not None:
            repeat_index = repeat_index.pk

        return StepType(
            step_id=step.pk,  # type: ignore
            name_nl=step.name_nl,  # type: ignore
            name_en=step.name_en,  # type: ignore
            description_nl=step.description_nl,  # type: ignore
            description_en=step.description_en,  # type: ignore
            slug=slug,
            repeat_index=repeat_index,  # type: ignore
            questions=questions,  # type: ignore
            substeps=substeps,  # type: ignore
            background=background,
        )

    def _resolve_step_questions(self, step, repeat_index):
        # TODO: make question instances from step, rather than questions
        # Check out the old implementation
        questions = []
        step_questions = list(BaseQuestion.objects.filter(step=step))
        for question in step_questions:
            questions.extend(self._make_question_instances(question))
        return questions

    def _make_question_instances(self, question: BaseQuestion, repeat_index) -> list:
        """Resolve all instances of a question (considering repeats).
        Also deletes hidden responses as a side effect."""

        if is_repeatable(question):
            return self._make_question_repeats(
                question,
                parent_index=repeat_index,
            )
        # When this question isn't repeatable, just return a single
        # instance
        instance = self._create_question_instance(
            question,
            repeat_index,
            background=False,
        )

        return [instance]

    def _make_question_repeats(
        self,
        question: BaseQuestion,
        parent_index=None,
    ):
        repeats = []
        # For repeatable questions, we first insert the "blank" background
        # step into the output.
        background_question = self._create_question_instance(
            question,
            repeat_index=parent_index,
            background=True,
        )
        repeats.append(background_question)
        # Then we continue by finding the question's
        # repeat_indices that correspond to this submission.
        repeat_indices = self._fetch_repeat_indices(
            question,
            parent_index=parent_index,
        )
        for index in repeat_indices:
            # Now we construct the step instances that will actually appear
            # because there are repeat indices for this question linked
            # to this submission.
            instance = self._create_question_instance(
                question,
                repeat_index=index,
                background=False,
            )
            repeats.append(instance)
        return repeats

    def _create_question_instance(
        self,
        question: BaseQuestion,
        repeat_index=None,
        background=False,
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
            "background": background,
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

        # Fallback (should not happen)
        return TextQuestionType(**base_data)

    def _fetch_repeat_indices(self, repeatable, parent_index=None):
        """
        Finds indices for the given object that are connected to
        the current submission.
        """
        # TODO: make this standalone with a submission argument
        submission = self.evaluator.submission
        if hasattr(repeatable, "repeatablestep"):
            repeatable = repeatable.repeatablestep
        indices = repeatable.repeat_indices.filter(
            submissions=submission,
        )
        if parent_index is not None:
            indices = indices.filter(parent=parent_index)
        return indices


# TODO: Move these helpers somewhere else
def generate_slug(
    sluggable,
    repeat_index=None,
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


def is_repeatable(step_or_question):
    """
    Determines if given step or question is repeatable.
    """
    if hasattr(step_or_question, "repeatablestep") or hasattr(
        step_or_question, "repeatablequestion"
    ):
        return True
    if issubclass(Repeatable, type(step_or_question)):
        return True
    if hasattr(step_or_question, "repeatable_ptr"):
        return True

    return False
