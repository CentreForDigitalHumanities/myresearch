from main.models import User, MRPermission

from django.db import models


class Study(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=200,
    )

    @staticmethod
    def can_be_created_by(user):
        return user.is_authenticated
