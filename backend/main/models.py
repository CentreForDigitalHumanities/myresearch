from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    # Some constants used for group names
    PRIVACY_OFFICER = "Privacy officer"
    FETC_MEMBER = "FETC member"

    @property
    def is_privacy_officer(self):
        return self.PRIVACY_OFFICER in [g.name for g in self.groups.all()]

    @property
    def is_fetc_member(self):
        return self.FETC_MEMBER in [g.name for g in self.groups.all()]


class MRPermission(models.TextChoices):
    """
    PermissionTypes are used in ObjectType's get_queryset method and Model's
    can_be_accessed_by() method, to decide which queryset gets returned or
    whether a user has access to an object, based on the user's permissions.
    """

    VIEW = "View"
    EDIT = "Edit"
