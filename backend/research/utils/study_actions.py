from research.other_models.reviews import SubmissionStatus
from main.models import MRPermission, User
from research.models import Study

#################################
# Base classes for StudyActions #
#################################


class StudyActions:
    """
    An object which can evaluate the available actions for a study and a user.
    """

    def __init__(self, study: Study, user: User):
        self.study = study
        self.user = user
        self.all_actions = [EditAction(study, user), DeleteAction(study, user)]

    def get_available_actions(self) -> list[str]:
        return [a.action_string for a in self.all_actions if a.is_available()]


class StudyAction:
    """
    An object containing the logic for making a specific action available and
    an action_string that gets passed to the frontend.

    Should be subclassed and not used directly.
    """

    action_string = ""

    def __init__(self, study, user):
        self.study = study
        self.user = user

    def is_available(
        self,
    ) -> bool:
        """Returns true if this action is available to the specified
        user given the current review."""

        return True


#################
# Study actions #
#################


class EditAction(StudyAction):

    action_string = "edit_action"

    def is_available(
        self,
    ):

        if (
            self.study in Study.objects.accessible_objects(self.user, MRPermission.EDIT)
            and self.study.status.status == SubmissionStatus.DRAFT
        ):
            return True

        return False


class DeleteAction(StudyAction):

    action_string = "delete_action"

    def is_available(
        self,
    ):

        if self.study in Study.objects.accessible_objects(self.user, MRPermission.EDIT):
            return True

        return False
