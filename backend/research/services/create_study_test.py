import pytest

from research.services.create_study import create_study
from research.models import Study
from research.other_models.reviews import StatusChange, SubmissionStatus
from form.models import UserFormSubmission


@pytest.mark.django_db
class TestCreateStudy:
    """Tests for create_study service"""

    def test_create_study_returns_study(self, test_user):
        """Test that create_study returns a Study object"""
        study = create_study(test_user)

        assert isinstance(study, Study)
        assert study.created_by == test_user

    def test_create_study_saves_to_database(self, test_user):
        """Test that the created study is saved to the database"""
        initial_count = Study.objects.count()
        study = create_study(test_user)

        assert Study.objects.count() == initial_count + 1
        assert Study.objects.get(id=study.id) == study

    def test_creates_form_submission(self, test_user, form):
        """Test that a UserFormSubmission is created"""
        initial_count = UserFormSubmission.objects.count()
        study = create_study(test_user)

        assert UserFormSubmission.objects.count() == initial_count + 1
        submission = UserFormSubmission.objects.get(study=study)
        assert submission.user == test_user
        assert submission.form == form

    def test_creates_status_change_with_draft_status(self, test_user):
        """Test that a StatusChange is created with DRAFT status"""
        initial_count = StatusChange.objects.count()
        study = create_study(test_user)

        assert StatusChange.objects.count() == initial_count + 1
        status_change = StatusChange.objects.get(study=study)
        assert status_change.status == SubmissionStatus.DRAFT
        assert status_change.created_by == test_user

    def test_submission_linked_to_study(self, test_user):
        """Test that the submission is linked to the study"""
        study = create_study(test_user)
        submission = UserFormSubmission.objects.get(study=study)

        assert submission.study == study

    def test_multiple_calls_create_separate_studies(self, test_user):
        """Test that calling create_study multiple times creates separate studies"""
        study1 = create_study(test_user)
        study2 = create_study(test_user)

        assert study1.id != study2.id
        assert Study.objects.filter(created_by=test_user).count() == 2

    def test_each_study_has_own_submission(self, test_user):
        """Test that each study has its own submission"""
        study1 = create_study(test_user)
        study2 = create_study(test_user)

        submission1 = UserFormSubmission.objects.get(study=study1)
        submission2 = UserFormSubmission.objects.get(study=study2)

        assert submission1.id != submission2.id

    def test_each_study_has_own_status_change(self, test_user):
        """Test that each study has its own status change"""
        study1 = create_study(test_user)
        study2 = create_study(test_user)

        status_change1 = StatusChange.objects.get(study=study1)
        status_change2 = StatusChange.objects.get(study=study2)

        assert status_change1.id != status_change2.id
