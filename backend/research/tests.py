import pytest
from django.contrib.auth.models import AnonymousUser, Group
from unittest.mock import MagicMock

from main.models import MRGroups, MRPermission, User
from research.models.study import YearCounter, Study
from research.models.reviews import StatusChange, SubmissionStatus
from form.models import Step, TextQuestion, QuestionResponse, UserFormSubmission

#################
# User fixtures #
#################


@pytest.fixture
def anonymous_user() -> AnonymousUser:
    return AnonymousUser()


@pytest.fixture
def po_user() -> User:
    po_user = User.objects.create_user(username="po_user", password="1234")
    po_group = Group.objects.get(name=MRGroups.PRIVACY_OFFICER)
    po_user.groups.add(po_group)
    return po_user


@pytest.fixture
def fetc_user() -> User:
    fetc_user = User.objects.create_user(username="fetc_user", password="1234")
    fetc_group = Group.objects.get(name=MRGroups.FETC_MEMBER)
    fetc_user.groups.add(fetc_group)
    return fetc_user


@pytest.fixture
def normal_user() -> User:
    return User.objects.create_user(username="user", password="1234")


##################
# Study fixtures #
##################


@pytest.fixture
def test_study(normal_user, form) -> Study:
    return Study.objects.create(created_by=normal_user)


@pytest.fixture
def test_po_study(po_user, form) -> Study:
    return Study.objects.create(created_by=po_user)


####################
# Permission Tests #
####################


@pytest.mark.django_db()
class TestStudyPermissions:
    def test_create_permission(self, anonymous_user: AnonymousUser, normal_user: User):
        """Test that users need to be authenticated to create a Study"""

        assert Study.can_be_created_by(anonymous_user) == False

        assert Study.can_be_created_by(normal_user) == True

    def _get_editable_and_viewable_studies(self, user):

        viewable_studies = Study.objects.accessible_objects(user, MRPermission.VIEW)
        editable_studies = Study.objects.accessible_objects(user, MRPermission.EDIT)
        return viewable_studies, editable_studies

    def test_anonymous_user_permissions(self, anonymous_user: AnonymousUser):
        """Test that anonymous_user cannot access any objects"""

        viewable_studies, editable_studies = self._get_editable_and_viewable_studies(
            anonymous_user
        )

        assert not viewable_studies

        assert not editable_studies

    def test_normal_user_permissions(self, normal_user: User, test_study: Study):
        """Test that normal user can only view and edit their own Study"""

        viewable_studies, editable_studies = self._get_editable_and_viewable_studies(
            normal_user
        )

        assert set(viewable_studies) == {test_study}

        assert set(editable_studies) == {test_study}

    def test_po_user_permissions(
        self, po_user: User, test_study: Study, test_po_study: Study
    ):
        """Test that po_user can view all studies and edit only their own Study"""

        viewable_studies, editable_studies = self._get_editable_and_viewable_studies(
            po_user
        )

        assert set(viewable_studies) == {test_study, test_po_study}

        assert set(editable_studies) == {test_po_study}

    def test_fetc_user_permissions(
        self, fetc_user: User, test_study: Study, test_po_study: Study
    ):
        """Test that fetc_user can view all studies and edit no studies (as
        they have not created any)"""

        viewable_studies, editable_studies = self._get_editable_and_viewable_studies(
            fetc_user
        )

        assert set(viewable_studies) == {test_study, test_po_study}

        assert not editable_studies


########################
# Reference Generation #
########################


@pytest.mark.django_db()
class TestStudyReferenceGeneration:
    """Tests for automatic reference number generation for Study objects."""

    def test_reference_generated_on_first_save(self, normal_user: User):
        """Test that a reference is generated when a Study is first saved."""
        study = Study(created_by=normal_user)

        # Before save, reference should be empty
        assert study.reference == ""

        # After save, reference should be populated
        study.save()
        assert study.reference != ""

    def test_reference_not_regenerated_on_subsequent_saves(self, normal_user: User):
        """Test that the reference is not regenerated when saving existing Study."""
        study = Study.objects.create(created_by=normal_user)
        original_reference = study.reference

        # Save again
        study.save()
        assert study.reference == original_reference

        # Modify and save again
        study.created_at  # Trigger any lazy operations
        study.save()
        assert study.reference == original_reference

    def test_counter_increments_for_multiple_studies(self, normal_user: User):
        """Test that counter increments for each new Study in the same year."""
        study1 = Study.objects.create(created_by=normal_user)
        study2 = Study.objects.create(created_by=normal_user)
        study3 = Study.objects.create(created_by=normal_user)

        # Extract counter numbers (last 4 digits)
        counter1 = int(study1.reference.split("-")[-1])
        counter2 = int(study2.reference.split("-")[-1])
        counter3 = int(study3.reference.split("-")[-1])

        # Counters should increment by 1
        assert counter2 == counter1 + 1
        assert counter3 == counter2 + 1

    def test_year_counter_created_on_demand(self, normal_user: User):
        """Test that YearCounter is created if it doesn't exist."""
        from django.utils import timezone

        current_year = timezone.now().year % 100

        # Delete YearCounter if it exists
        YearCounter.objects.filter(year=current_year).delete()

        # Create a study
        study = Study.objects.create(created_by=normal_user)

        # YearCounter should now exist
        year_counter = YearCounter.objects.get(year=current_year)
        assert year_counter.counter >= 1

    def test_concurrent_save_generates_unique_references(self, normal_user: User):
        """Test that concurrent saves generate unique references (via row locking)."""
        # This is a basic test; full concurrency testing would require threading
        from django.utils import timezone

        current_year = timezone.now().year % 100
        YearCounter.objects.filter(year=current_year).delete()

        # Create multiple studies in rapid succession
        references = set()
        for i in range(10):
            study = Study.objects.create(created_by=normal_user)
            references.add(study.reference)

        # All references should be unique
        assert len(references) == 10, "Duplicate references found in concurrent saves"


###########################
# StudyManager Annotations #
###########################


@pytest.mark.django_db(transaction=True)
class TestStudyManagerAnnotations:
    """Tests for StudyManager annotation methods."""

    def test_annotation_key_creates_study_attributes(self, form, normal_user):
        """Test that questions with annotation_key become attributes on Study."""
        step = Step.objects.create(name="Step", slug="step", form=form)

        # Create questions with annotation keys
        q1 = TextQuestion.objects.create(
            text="Study Name",
            step=step,
            annotation_key="study_name",
        )
        q2 = TextQuestion.objects.create(
            text="Location",
            step=step,
            annotation_key="location",
        )

        # Create a study and submission
        study = Study.objects.create(created_by=normal_user)
        submission = UserFormSubmission.objects.create(
            user=normal_user,
            form=form,
            study=study,
        )

        # Create responses for both questions
        response1 = QuestionResponse.objects.create(
            question=q1,
            answer={"value": "My Study"},
        )
        response1.submissions.add(submission)

        response2 = QuestionResponse.objects.create(
            question=q2,
            answer={"value": "Berlin"},
        )
        response2.submissions.add(submission)

        # Retrieve study from queryset with annotations
        study_with_annotations = Study.objects.get(pk=study.pk)

        # Check that annotations are present
        assert hasattr(study_with_annotations, "study_name")
        assert hasattr(study_with_annotations, "location")
        assert study_with_annotations.study_name == "My Study"
        assert study_with_annotations.location == "Berlin"

    def test_empty_annotation_key_excluded(self, form, normal_user):
        """Test that questions with empty annotation_key are not annotated."""
        step = Step.objects.create(name="Step", slug="step", form=form)

        # Create question with empty annotation_key
        q1 = TextQuestion.objects.create(
            text="Question without key",
            step=step,
            annotation_key="",
        )

        study = Study.objects.create(created_by=normal_user)
        submission = UserFormSubmission.objects.create(
            user=normal_user,
            form=form,
            study=study,
        )

        response = QuestionResponse.objects.create(
            question=q1,
            answer={"value": "Some answer"},
        )
        response.submissions.add(submission)

        study_with_annotations = Study.objects.get(pk=study.pk)

        # Empty annotation_key should not create an attribute
        assert not hasattr(study_with_annotations, "")

    def test_latest_answer_retrieved(self, form, normal_user):
        """Test that the latest answer is retrieved for each annotation_key."""
        step = Step.objects.create(name="Step", slug="step", form=form)

        q1 = TextQuestion.objects.create(
            text="Name",
            step=step,
            annotation_key="name",
        )

        study = Study.objects.create(created_by=normal_user)
        submission = UserFormSubmission.objects.create(
            user=normal_user,
            form=form,
            study=study,
        )

        # Create multiple responses for the same question
        response1 = QuestionResponse.objects.create(
            question=q1,
            answer={"value": "First Name"},
        )
        response1.submissions.add(submission)

        response2 = QuestionResponse.objects.create(
            question=q1,
            answer={"value": "Latest Name"},
        )
        response2.submissions.add(submission)

        study_with_annotations = Study.objects.get(pk=study.pk)

        # Should get the latest answer
        assert study_with_annotations.name == "Latest Name"

    def test_default_title_annotation(self, form, normal_user):
        """Test that default title is provided when no title annotation exists."""

        study = Study.objects.create(created_by=normal_user)

        study_with_annotations = Study.objects.get(pk=study.pk)

        # Should have a default title
        assert hasattr(study_with_annotations, "title")
        assert study_with_annotations.title is not None
        assert "Study created on" in study_with_annotations.title

    def test_title_annotation_overrides_default(self, form, normal_user):
        """Test that explicit title annotation overrides default."""
        # Set the form's study_name_question to a question with annotation_key 'title'
        step = Step.objects.create(name="Step", slug="step", form=form)

        title_q = TextQuestion.objects.create(
            text="Study Title",
            step=step,
            annotation_key="title",
        )

        study = Study.objects.create(created_by=normal_user)
        submission = UserFormSubmission.objects.create(
            user=normal_user,
            form=form,
            study=study,
        )

        response = QuestionResponse.objects.create(
            question=title_q,
            answer={"value": "Custom Title"},
        )
        response.submissions.add(submission)

        study_with_annotations = Study.objects.get(pk=study.pk)

        # Should have custom title
        assert study_with_annotations.title == "Custom Title"


##############################
# DeleteStudy Mutation Tests #
##############################

DELETE_STUDY_MUTATION = """
    mutation DeleteStudy($id: ID!) {
        deleteStudy(id: $id) {
            ok
            errors {
                field
                messages
            }
        }
    }
"""


def _make_context(user):
    """Return a mock request context with the given user."""
    request = MagicMock()
    request.user = user
    return request


@pytest.mark.django_db()
class TestDeleteStudyMutation:
    """Tests for the DeleteStudy GraphQL mutation."""

    def _execute(self, user, study_id):
        from api.graphql.schema import schema

        result = schema.execute(
            DELETE_STUDY_MUTATION,
            variable_values={"id": study_id},
            context_value=_make_context(user),
        )
        return result

    def test_hard_delete_unsubmitted_study(self, normal_user: User, test_study: Study):
        """Owner can hard-delete a study that has never been submitted."""
        study_id = test_study.pk

        result = self._execute(normal_user, study_id)

        assert not result.errors
        assert result.data
        assert result.data["deleteStudy"]["ok"] is True
        assert not result.data["deleteStudy"]["errors"]
        assert not Study.objects.filter(pk=study_id).exists()

    def test_soft_delete_submitted_study(self, normal_user: User, test_study: Study):
        """
        Owner cannot soft-delete a study that has been submitted.
        """
        StatusChange.objects.create(
            study=test_study,
            status=SubmissionStatus.SUBMITTED,
            created_by=normal_user,
        )

        result = self._execute(normal_user, test_study.pk)

        assert result.data
        assert result.data["deleteStudy"]["ok"] is False
        assert result.data["deleteStudy"]["errors"]

        test_study.refresh_from_db()
        assert test_study.is_deleted is False

    def test_delete_another_users_study_returns_error(
        self, normal_user: User, test_po_study: Study
    ):
        """A user cannot delete a study that belongs to another user."""
        result = self._execute(normal_user, test_po_study.pk)

        assert not result.errors
        assert result.data
        assert result.data["deleteStudy"]["ok"] is False
        assert result.data["deleteStudy"]["errors"]
        assert Study.objects.filter(pk=test_po_study.pk).exists()

    def test_delete_nonexistent_study_returns_error(self, normal_user: User):
        """Attempting to delete a non-existent study ID returns an error."""
        result = self._execute(normal_user, 999999)

        assert not result.errors
        assert result.data
        assert result.data["deleteStudy"]["ok"] is False
        assert result.data["deleteStudy"]["errors"]

    def test_anonymous_user_cannot_delete(
        self, anonymous_user: AnonymousUser, test_study: Study
    ):
        """An unauthenticated user cannot delete any study."""
        study_id = test_study.pk

        result = self._execute(anonymous_user, study_id)

        assert not result.errors
        assert result.data
        assert result.data["deleteStudy"]["ok"] is False
        assert result.data["deleteStudy"]["errors"]
        assert Study.objects.filter(pk=study_id).exists()
