from abc import ABC, abstractmethod

from graphene import Enum

from research.models.reviews import SubmissionStatus
from main.models import MRPermission, User
from research.models.study import Study


class ActionEnum(Enum):
    EDIT_ACTION = "edit_action"
    DELETE_ACTION = "delete_action"
    RETURN_TO_DRAFT_ACTION = "return_to_draft_action"
    MARK_SEEN_ACTION = "mark_seen_action"
    MARK_UNSEEN_ACTION = "mark_unseen_action"


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
        self.all_actions = [
            StudyEditAction,
            StudyDeleteAction,
            ReturnToDraftAction,
            MarkSeenAction,
            MarkUnseenAction,
        ]

    def get_available_actions(self) -> list[ActionEnum]:
        return [
            a.action for a in self.all_actions if a.is_available(self.study, self.user)
        ]


class StudyAction(ABC):
    """
    An object containing the logic for making a specific action available and
    an action that gets passed to the frontend.

    Should be subclassed and not used directly.
    """

    action: ActionEnum

    @classmethod
    @abstractmethod
    def is_available(cls, study, user) -> bool:
        """Returns true if this action is available to the specified
        user given the current review."""

        return True


#################
# Study actions #
#################


class StudyEditAction(StudyAction):
    action = ActionEnum.EDIT_ACTION

    @classmethod
    def is_available(cls, study, user):

        return (
            study in Study.objects.accessible_objects(user, MRPermission.EDIT)
            and study.status == SubmissionStatus.DRAFT
        )


class StudyDeleteAction(StudyAction):
    action = ActionEnum.DELETE_ACTION

    @classmethod
    def is_available(cls, study, user):
        return study in Study.objects.accessible_objects(user, MRPermission.DELETE)


class PrivacyOfficerStudyAction(StudyAction):
    """Base class for actions that require privacy officer permission."""

    @classmethod
    def is_available(
        cls,
        study,
        user,
    ) -> bool:
        if study.status == SubmissionStatus.DRAFT:
            return False

        if not user.is_privacy_officer:
            return False

        return True


class ReturnToDraftAction(PrivacyOfficerStudyAction):

    action = ActionEnum.RETURN_TO_DRAFT_ACTION


class MarkSeenAction(PrivacyOfficerStudyAction):

    action = ActionEnum.MARK_SEEN_ACTION

    @classmethod
    def is_available(cls, study, user):

        if study.is_seen:
            return False

        return super().is_available(study, user)


class MarkUnseenAction(PrivacyOfficerStudyAction):

    action = ActionEnum.MARK_UNSEEN_ACTION

    @classmethod
    def is_available(cls, study, user):

        if not study.is_seen:
            return False

        return super().is_available(study, user)
