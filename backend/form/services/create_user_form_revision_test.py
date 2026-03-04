import pytest

from form.services.create_user_form_revision import create_user_form_revision
from form.services.update_submission import update_or_create_submission
from form.mutations.utils.inputs import UserFormInput
from form.models import UserFormSubmission, QuestionResponse


@pytest.mark.django_db
class TestCreateRevision:
    """
    Tests for create_user_from_revision service
    """

    def test_revise_user_form_input(
        self,
        test_user,
        user_form_input,
    ):
        """Test creation of revision of UserFormSubmission"""

        submission = update_or_create_submission(test_user, user_form_input)
        submission_revision = create_user_form_revision(submission.id)

        assert submission_revision.user == test_user
        assert submission_revision != submission
        assert set(submission.responses.all()) == set(
            submission_revision.responses.all()
        )

    def test_update_revision_response(self, test_user, user_form_input):
        """Test updating an aswer for revision"""

        submission = update_or_create_submission(test_user, user_form_input)
        old_response = QuestionResponse.objects.filter(submissions=submission).first()

        submission_revision = create_user_form_revision(submission.id)

        assert old_response in submission_revision.responses.all()

        user_form_input["submission_id"] = submission_revision.id
        user_form_input["responses"][0]["id"] = old_response.id

        # If we update the revision, but the answer remains the same, the old
        # response should remain intact.

        updated_revision = update_or_create_submission(test_user, user_form_input)

        assert updated_revision == submission_revision
        assert set(updated_revision.responses.all()) == set(
            submission_revision.responses.all()
        )

        # If we add a new answer, a new response should get made
        new_ans = {"value": "new_answer"}
        user_form_input["responses"][0]["answer"] = new_ans

        updated_revision = update_or_create_submission(test_user, user_form_input)
        new_response = QuestionResponse.objects.filter(
            submissions=updated_revision
        ).first()

        assert updated_revision.responses.count() == 1
        assert old_response not in updated_revision.responses.all()
        assert new_response.id != old_response.id
        assert new_response.answer != old_response.answer
        assert new_response.answer == new_ans
