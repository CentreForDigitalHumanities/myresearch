from graphene import ObjectType

from form.models import BaseQuestion, Step, QuestionResponse
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

    def _create_question_instance(
        self, question: BaseQuestion, repeat_index: int
    ) -> ObjectType:
        """Create the appropriate user question instance type based on the question type."""
        response = self.evaluator.get_user_response(question, repeat_index)

        base_data = {
            "question_id": question.pk,
            "repeat_index": repeat_index,
            "answer": response.answer if response else None,
            "response_id": response.pk if response else None,
            # The 'question' field is used for BaseQuestionInterface.resolve_type.
            "question": question,
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

    def resolve(self) -> UserFormType:
        """Resolve the complete user form structure."""
        form = self.evaluator.form
        submission = self.evaluator.submission

        steps = []
        for step in Step.objects.filter(form=form, parent__isnull=True).all():
            steps.extend(self._resolve_step_instances(step))

        return UserFormType(
            form_id=form.pk,  # type: ignore
            name_nl=form.name_nl,  # type: ignore
            name_en=form.name_en,  # type: ignore
            steps=steps,  # type: ignore
            submission_id=submission.pk if submission else None,  # type: ignore
            started_at=submission.started_at if submission else None,  # type: ignore
            completed_at=submission.completed_at if submission else None,  # type: ignore
        )

    def _resolve_step_instances(self, step: Step) -> list[StepType]:
        """Resolve all instances of a step (considering repeats)."""
        if not self.evaluator.is_step_visible(step):
            return []

        step_questions = list(BaseQuestion.objects.filter(step=step))
        step_substeps = list(Step.objects.filter(parent=step).all())

        repeat_count = self.evaluator.get_repeat_count_for_step(step)
        instances = []

        for repeat_index in range(repeat_count):
            # Get all questions
            questions = []
            for question in step_questions:
                questions.extend(self._resolve_question_instances(question))

            # Get all substeps
            substeps = []
            for substep in step_substeps:
                substeps.extend(self._resolve_step_instances(substep))

            instances.append(
                StepType(
                    step_id=step.pk,  # type: ignore
                    name_nl=step.name_nl,  # type: ignore
                    name_en=step.name_en,  # type: ignore
                    description_nl=step.description_nl,  # type: ignore
                    description_en=step.description_en,  # type: ignore
                    slug=(  # type: ignore
                        f"{step.slug}-{repeat_index}" if repeat_index > 0 else step.slug
                    ),
                    repeat_index=repeat_index,  # type: ignore
                    questions=questions,  # type: ignore
                    substeps=substeps,  # type: ignore
                )
            )

        return instances

    def _resolve_question_instances(self, question: BaseQuestion) -> list:
        """Resolve all instances of a question (considering repeats).
        Also, deletes hidden response."""

        # non-repeating questions have a repeat count as well
        repeat_count = self.evaluator.get_repeat_count_for_question(question)

        # If a response is hidden it should be removed to prevent errors triggering on invisible questions.
        if not self.evaluator.is_question_visible(question):
            QuestionResponse.objects.filter(
                submissions__in=[self.evaluator.submission],
                question=question,
            ).delete()
            return []


        # if len(question_responses) > repeat_count:
        #      for response in question_responses:
        #          if (response.repeat_index + 1) > repeat_count:
        #              print("deleting response: " + response.__str__() + " in question: " + question.__str__())
        #              response.delete()



        instances = []
        for repeat_index in range(repeat_count):
            instance = self._create_question_instance(question, repeat_index)
            instances.append(instance)

        return instances