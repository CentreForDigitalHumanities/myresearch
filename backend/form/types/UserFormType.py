from graphene import (
    ID,
    Field,
    Int,
    ObjectType,
    ResolveInfo,
    String,
    List,
    DateTime,
    NonNull,
)

from form.models import (
    Step,
    BaseQuestion,
    SelectQuestion,
    TrueFalseQuestion,
    TextQuestion,
    NumberQuestion,
    DateQuestion,
    FileUploadQuestion,
)
from form.services.form_evaluator import FormEvaluator
from form.types.StepType import StepType
from form.types.UserQuestionType import (
    BaseUserQuestionInterface,
    UserDateQuestionType,
    UserFileUploadQuestionType,
    UserSelectQuestionType,
    UserTextQuestionType,
    UserNumberQuestionType,
    UserTrueFalseQuestionType,
    UserQuestionType,
)


class UserStepType(ObjectType):
    """Represents a single instance of a step for a user (accounting for repeats)."""

    step_id = ID(required=True)
    name_nl = String(required=True)
    name_en = String(required=True)
    description_nl = String()
    description_en = String()
    slug = String(required=True)
    repeat_index = Int(required=True)

    questions = List(
        NonNull(BaseUserQuestionInterface),
        required=True,
    )
    substeps = List(
        lambda: NonNull(UserStepType),
        required=True,
    )


class UserFormType(ObjectType):
    """The form structure as it appears to a specific user."""

    form_id = ID(required=True)
    name_nl = String(required=True)
    name_en = String(required=True)
    steps = List(
        NonNull(UserStepType),
        required=True,
    )
    submission_id = ID()
    started_at = DateTime()
    completed_at = DateTime()


class UserFormResolver:
    """Helper to resolve user-specific form structure."""

    def __init__(self, evaluator: FormEvaluator):
        self.evaluator = evaluator

    def _create_question_instance(
        self, question: BaseQuestion, repeat_index: int
    ) -> ObjectType:
        """Create the appropriate user question instance type based on the question type."""
        answer = self.evaluator.get_user_answer(question, repeat_index)

        base_data = {
            "question_id": question.pk,
            "repeat_index": repeat_index,
            "answer": answer,
            "question": question,  # Pass the question object for field resolution
        }

        # Access the specific subclass using Django's reverse relation attributes
        if hasattr(question, "textquestion"):
            return UserTextQuestionType(**base_data)
        elif hasattr(question, "numberquestion"):
            return UserNumberQuestionType(**base_data)
        elif hasattr(question, "truefalsequestion"):
            return UserTrueFalseQuestionType(**base_data)
        elif hasattr(question, "datequestion"):
            return UserDateQuestionType(**base_data)
        elif hasattr(question, "selectquestion"):
            return UserSelectQuestionType(**base_data)
        elif hasattr(question, "fileuploadquestion"):
            return UserFileUploadQuestionType(**base_data)

        # Fallback (should not happen)
        return UserTextQuestionType(**base_data)

    def resolve_question_instances(self, question: BaseQuestion) -> list:
        """Resolve all instances of a question (considering repeats)."""
        if not self.evaluator.is_question_visible(question):
            return []

        repeat_count = self.evaluator.get_repeat_count_for_question(question)
        instances = []

        for repeat_index in range(repeat_count):
            instance = self._create_question_instance(question, repeat_index)
            instances.append(instance)

        return instances

    def resolve_steps(self) -> list[UserStepType]:
        form = self.evaluator.form

        steps = []
        for step in Step.objects.filter(form=form, parent__isnull=True).all():
            steps.extend(self._resolve_step_instances(step))

        return steps

    def _resolve_step_instances(self, step: Step) -> list[UserStepType]:
        """Resolve all instances of a step (considering repeats)."""
        if not self.evaluator.is_step_visible(step):
            return []

        repeat_count = self.evaluator.get_repeat_count_for_step(step)
        instances = []

        for repeat_index in range(repeat_count):
            # Get all questions for this step instance
            questions = []
            for question in BaseQuestion.objects.filter(step=step):
                questions.extend(self.resolve_question_instances(question))

            # Get all substeps for this step instance
            substeps = []
            for substep in Step.objects.filter(parent=step).all():
                substeps.extend(self._resolve_step_instances(substep))

            instances.append(
                UserStepType(
                    step_id=step.pk,
                    name_nl=step.name_nl,
                    name_en=step.name_en,
                    description_nl=step.description_nl,
                    description_en=step.description_en,
                    slug=(
                        f"{step.slug}-{repeat_index}" if repeat_index > 0 else step.slug
                    ),
                    repeat_index=repeat_index,
                    questions=questions,
                    substeps=substeps,
                )
            )

        return instances
