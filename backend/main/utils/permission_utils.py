from main.models import User, MRPermission

from django.db import models


class BaseMRManager(models.Manager):
    """
    A Base manager class for handling object permissions.

    _viewable_objects and _editable_objects should be overwritten to contain
    the permission logic for a specific model. We can then get a filtered
    queryset of objects, based on the users permissions via accessible_objects.
    """

    def accessible_objects(self, user: User, mr_permission):
        """
        A base method redirecting to filters based on specific mr_permission's
        """

        # If a user is not authenticated, return no objects
        if not user.is_authenticated:
            return self.none()
        match mr_permission:
            case MRPermission.VIEW:
                return self._viewable_objects(user)
            case MRPermission.EDIT:
                return self._editable_objects(user)

        # NOTE: This should never happen.
        raise ValueError(
            "accessible_objects() has received a permission type which has not "
            "yet been implemented."
        )

    def _viewable_objects(self, user: User):
        # Needs to be overwritten for a specific object's permissions
        return self.all()

    def _editable_objects(self, user: User):
        # Needs to be overwritten for a specific object's permissions
        return self.all()
