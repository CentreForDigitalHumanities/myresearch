from graphene import Field, List, Mutation, ResolveInfo, JSONString, ID, Boolean
from graphene_django.types import ErrorType

from form.models import MRForm, UserFormSubmission, QuestionResponse, BaseQuestion
from form.services.form_evaluator import FormEvaluator
from form.types.UserFormType import UserFormType, UserFormResolver


def validate_answers(answers: list, form: MRForm) -> tuple[list[dict], list[ErrorType]]:
    """
    Validate user answers for a form submission.

    Args:
        answers: List of answer objects with question_id, repeat_index, and answer
        form: The MRForm to validate against

    Returns:
        Tuple of (valid_answers, errors) where:
        - valid_answers: List of validated answer dicts with question, repeat_index, answer
        - errors: List of ErrorType objects for any validation failures
    """
    errors = []
    valid_answers = []

    # Validate that answers is a list
    if not isinstance(answers, list):
        errors.append(
            ErrorType(
                field="answers",
                messages=["Answers must be a list of question responses."],
            )
        )
        return valid_answers, errors

    # Validate each answer
    for idx, answer_data in enumerate(answers):
        # Validate structure
        if not isinstance(answer_data, dict):
            errors.append(
                ErrorType(
                    field=f"answers[{idx}]",
                    messages=["Each answer must be an object."],
                )
            )
            continue

        question_id = answer_data.get("question_id")
        repeat_index = answer_data.get("repeat_index", 0)
        answer = answer_data.get("answer")

        # Validate required fields
        if not question_id:
            errors.append(
                ErrorType(
                    field=f"answers[{idx}].question_id",
                    messages=["question_id is required."],
                )
            )
            continue

        if answer is None:
            errors.append(
                ErrorType(
                    field=f"answers[{idx}].answer",
                    messages=["answer is required."],
                )
            )
            continue

        # Validate question exists
        try:
            question = BaseQuestion.objects.get(pk=question_id)
        except BaseQuestion.DoesNotExist:
            errors.append(
                ErrorType(
                    field=f"answers[{idx}].question_id",
                    messages=[f"Question with id {question_id} does not exist."],
                )
            )
            continue

        # Validate question belongs to this form
        if question.step.top_form.pk != form.pk:
            errors.append(
                ErrorType(
                    field=f"answers[{idx}].question_id",
                    messages=[
                        f"Question {question_id} does not belong to form {form.pk}."
                    ],
                )
            )
            continue

        # Validate required questions have non-empty answers
        if question.required and not answer:
            errors.append(
                ErrorType(
                    field=f"answers[{idx}].answer",
                    messages=[f"Question '{question.text}' is required."],
                )
            )
            continue

        # If all validations pass, add to valid answers
        valid_answers.append(
            {
                "question": question,
                "repeat_index": repeat_index,
                "answer": answer,
            }
        )

    return valid_answers, errors


class SubmitUserFormMutation(Mutation):
    """
    Mutation to submit user answers to a form.

    Input format for answers:
    [
        {
            "question_id": "1",
            "repeat_index": 0,
            "answer": {"value": "some answer"}
        },
        {
            "question_id": "2",
            "repeat_index": 0,
            "answer": {"option_ids": [1, 2]}
        }
    ]
    """

    user_form = Field(UserFormType)
    success = Boolean()
    errors = List(ErrorType)

    class Arguments:
        form_id = ID(required=True)
        answers = JSONString(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        form_id: str,
        answers: list,
    ):
        user = info.context.user

        # Check authentication
        if not user.is_authenticated:
            error = ErrorType(
                field="user",
                messages=["You must be authenticated to submit a form."],
            )
            return cls(success=False, errors=[error])

        # Get the form
        try:
            form = MRForm.objects.get(pk=form_id)
        except MRForm.DoesNotExist:
            error = ErrorType(
                field="form_id",
                messages=[f"Form with id {form_id} does not exist."],
            )
            return cls(success=False, errors=[error])

        valid_answers, errors = validate_answers(answers, form)

        if errors:
            return cls(success=False, errors=errors)

        evaluator = FormEvaluator(form, user, create_submission=True)
        submission = evaluator.submission

        cls.save_answers_and_submission(valid_answers, submission)

        user_form = cls.get_updated_user_form(evaluator)

        return cls(success=True, user_form=user_form, errors=[])

    @classmethod
    def save_answers_and_submission(
        cls,
        valid_answers: list[dict],
        submission: UserFormSubmission,
    ) -> None:
        """Saves answers to DB and updates submission timestamp."""
        for answer_data in valid_answers:
            QuestionResponse.objects.update_or_create(
                submission=submission,
                question=answer_data["question"],
                repeat_index=answer_data["repeat_index"],
                defaults={"answer": answer_data["answer"]},
            )

        submission.save()

    @classmethod
    def get_updated_user_form(cls, evaluator: FormEvaluator) -> UserFormType:
        """Gets updated UserFormType to send to the frontend."""
        form = evaluator.form
        submission = evaluator.submission
        
        resolver = UserFormResolver(evaluator)
        steps = resolver.resolve_steps()

        user_form = UserFormType(
            form_id=form.pk,
            name=form.name,
            steps=steps,
            submission_id=submission.pk,
            started_at=submission.started_at,
            completed_at=submission.completed_at,
        )

        return user_form
