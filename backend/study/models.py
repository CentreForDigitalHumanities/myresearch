from main.models import User, MRPermission

from django.db import models


class Study(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=200,
    )

    def can_be_accessed_by(self, user, permission):
        """
        Check whether an object can be accessed by a specific user, with a
        specific permission type.

        TODO: This function should probably live in some kind off mixin for all
        models in MyResearch.
        """
        if not user.is_authenticated:
            return False
        if permission == MRPermission.EDIT:
            return self.can_be_edited_by(user)
        if permission == MRPermission.VIEW:
            return self.can_be_viewed_by(user)
        raise ValueError(
            f"{self}.can_be_accessed_by() has received a permission type which "
            "has not yet been implemented."
        )

    def can_be_viewed_by(self, user):

        if user == self.created_by:
            return True
        if user.is_privacy_officer or user.is_fetc_member:
            return True
        return False

    def can_be_edited_by(self, user):

        if user == self.created_by:
            return True
        return False
