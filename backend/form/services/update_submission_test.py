import pytest

from form.services.update_submission import update_submission
from form.models import UserFormSubmission, QuestionResponse


@pytest.mark.django_db
class TestUpdateSubmission:
    """
    Tests for update_or_create_submission service
    """

    def test_update_response(self, test_user, user_form_input):
        """Test updating an answer"""

        submission = update_submission(test_user, user_form_input)
        response = QuestionResponse.objects.filter(submissions=submission).first()

        new_ans = {"value": "new_answer"}

        user_form_input["submission_id"] = submission.id
        user_form_input["responses"][0]["id"] = response.id
        user_form_input["responses"][0]["answer"] = new_ans

        old_ans = response.answer
        old_response_id = response.id

        submission = update_submission(test_user, user_form_input)
        response = QuestionResponse.objects.filter(submissions=submission).first()

        assert submission.responses.count() == 1
        assert old_response_id == response.id
        assert response.answer != old_ans
        assert response.answer == new_ans
