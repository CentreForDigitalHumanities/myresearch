from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def is_privacy_officer(
        self,
    ):
        return "Privacy officer" in [g.name for g in self.groups.all()]

    @property
    def is_fetc_member(
        self,
    ):
        return "FETC member" in [g.name for g in self.groups.all()]


class MRPermissionTypes(models.IntegerChoices):
    """
    PermissionTypes are used in ObjectType's get_queryset method, to decide
    which queryset gets returned, based on the user's permissions.
    """

    VIEW = 1
    EDIT = 2
