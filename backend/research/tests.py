import pytest
import re
from datetime import datetime
from unittest.mock import patch
from django.contrib.auth.models import AnonymousUser, Group
from django.db import transaction

from main.models import MRGroups, MRPermission, User
from research.other_models.utils import YearCounter
from .models import Study

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
