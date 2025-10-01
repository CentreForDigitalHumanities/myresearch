from main.models import User

from django.db import models

class Study (models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField()

    def can_be_viewed_by(self, user):

        if user == self.created_by:
            return True
        if user.is_privacy_officer:
            return True
        return False
    
    def can_be_edited_by(self, user):

        if user == self.created_by:
            return True
        return False