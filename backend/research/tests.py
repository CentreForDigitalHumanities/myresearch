import pytest
from django.test import TestCase
from django.db import IntegrityError, transaction
from django.contrib.auth.models import AnonymousUser, Group

from main.models import MRGroups, MRPermission, User
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
def test_study(normal_user) -> Study:
    return Study.objects.create(title="normal_user's study", created_by=normal_user)


@pytest.fixture
def test_po_study(po_user) -> Study:
    return Study.objects.create(title="po_user's study", created_by=po_user)


####################
# Permission Tests #
####################


@pytest.mark.django_db()
class TestStudyPermissions:
    def test_create_permission(
        self, anonymous_user: AnonymousUser, normal_user: User
    ):
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
