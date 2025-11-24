from graphene import (
    ID,
    Int,
    ObjectType,
    String,
    Boolean,
    List,
    DateTime,
    JSONString,
    NonNull,
)

from form.models import (
    SelectOption,
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


class UserQuestionInstanceType(ObjectType):
    """Represents a single instance of a question for a user (accounting for repeats)."""

    question_id = ID(required=True)
    repeat_index = Int(required=True)

    # User's answer (if any)
    answer = JSONString()

    # Resolved fields from the associated question
    question_type = String(required=True)
    text = String(required=True)
    description = String()
    required = Boolean(required=True)
    question_data = JSONString(
        description="Type-specific question data (options, placeholder, etc.)"
    )

    def resolve_question_type(self, info):
        question = BaseQuestion.objects.get(pk=self.question_id)
        resolver = UserFormResolver(self.evaluator)
        return resolver._get_question_type_name(question)

    def resolve_text(self, info):
        question = BaseQuestion.objects.get(pk=self.question_id)
        return question.text

    def resolve_description(self, info):
        question = BaseQuestion.objects.get(pk=self.question_id)
        return question.description

    def resolve_required(self, info):
        question = BaseQuestion.objects.get(pk=self.question_id)
        return question.required

    def resolve_question_data(self, info):
        question = BaseQuestion.objects.get(pk=self.question_id)
        resolver = UserFormResolver(self.evaluator)
        return resolver._get_question_data(question)


class UserStepInstanceType(ObjectType):
    """Represents a single instance of a step for a user (accounting for repeats)."""

    step_id = ID(required=True)
    name = String(required=True)
    description = String()
    slug = String(required=True)
    repeat_index = Int(required=True)

    questions = List(
        NonNull(UserQuestionInstanceType),
        required=True,
    )
    substeps = List(
        lambda: NonNull(UserStepInstanceType),
        required=True,
    )


class UserFormType(ObjectType):
    """The form structure as it appears to a specific user."""

    form_id = ID(required=True)
    name = String(required=True)
    steps = List(
        NonNull(UserStepInstanceType),
        required=True,
    )
    submission_id = ID()
    started_at = DateTime()
    completed_at = DateTime()


class UserFormResolver:
    """Helper to resolve user-specific form structure."""

    def __init__(self, evaluator: FormEvaluator):
        self.evaluator = evaluator

    def _get_question_type_name(self, question: BaseQuestion) -> str:
        """Get the concrete question type name."""
        if isinstance(question, SelectQuestion):
            return "select"
        elif isinstance(question, TrueFalseQuestion):
            return "truefalse"
        elif isinstance(question, TextQuestion):
            return "text"
        elif isinstance(question, NumberQuestion):
            return "number"
        elif isinstance(question, DateQuestion):
            return "date"
        elif isinstance(question, FileUploadQuestion):
            return "fileupload"
        return "base"

    def _get_question_data(self, question: BaseQuestion) -> dict:
        """Get type-specific question data."""
        data = {}

        if isinstance(question, SelectQuestion):
            data["multiple"] = question.multiple
            data["options"] = [
                {
                    "id": opt.pk,
                    "label": opt.label,
                    "default_selected": opt.default_selected,
                }
                for opt in SelectOption.objects.filter(question=question).all()
            ]
        elif isinstance(question, TextQuestion):
            data["placeholder"] = question.placeholder
            data["lines"] = question.lines
        elif isinstance(question, NumberQuestion):
            data["positive_only"] = question.positive_only
        elif isinstance(question, DateQuestion):
            data["future_only"] = question.future_only
        elif isinstance(question, FileUploadQuestion):
            data["size_limit"] = question.size_limit
        elif isinstance(question, TrueFalseQuestion):
            data["default_value"] = question.default_value

        return data

    def resolve_question_instances(
        self, question: BaseQuestion
    ) -> list[UserQuestionInstanceType]:
        """Resolve all instances of a question (considering repeats)."""
        if not self.evaluator.is_question_visible(question):
            return []

        repeat_count = self.evaluator.get_repeat_count_for_question(question)
        instances = []

        for repeat_index in range(repeat_count):
            instance = UserQuestionInstanceType(
                question_id=question.pk,
                repeat_index=repeat_index,
                answer=self.evaluator.get_user_answer(question, repeat_index),
            )
            instance.evaluator = self.evaluator
            instances.append(instance)

        return instances

    def resolve_steps(self) -> list[UserStepInstanceType]:
        form = self.evaluator.form

        steps = []
        for step in Step.objects.filter(form=form, parent__isnull=True).all():
            steps.extend(self._resolve_step_instances(step))

        return steps

    def _resolve_step_instances(self, step: Step) -> list[UserStepInstanceType]:
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
                UserStepInstanceType(
                    step_id=step.pk,
                    name=step.name,
                    description=step.description,
                    slug=(
                        f"{step.slug}-{repeat_index}" if repeat_index > 0 else step.slug
                    ),
                    repeat_index=repeat_index,
                    questions=questions,
                    substeps=substeps,
                )
            )

        return instances
