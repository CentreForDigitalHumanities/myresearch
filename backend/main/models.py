from django.contrib.auth.models import AbstractUser
from django.db import models


class MRGroups(models.TextChoices):
    PRIVACY_OFFICER = "Privacy officer"
    FETC_MEMBER = "FETC member"


class User(AbstractUser):
    @property
    def is_privacy_officer(self):
        return MRGroups.PRIVACY_OFFICER in [g.name for g in self.groups.all()]

    @property
    def is_fetc_member(self):
        return MRGroups.FETC_MEMBER in [g.name for g in self.groups.all()]

    def has_access_to(self, object, mrpermission):
        """
        Utility function to check if a user has access to a specific object,
        with a specific permission.
        """
        return object in object.__class__.objects.accessible_objects(self, mrpermission)


class MRPermission(models.TextChoices):
    """
    PermissionTypes are used in ObjectType's get_queryset method, to decide
    which queryset gets returned or whether a user has access to an object,
    based on the user's permissions.
    """

    VIEW = "View"
    EDIT = "Edit"
