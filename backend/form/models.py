from django.db import models
from django.db.models import QuerySet, Q
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

user_model = get_user_model()

class MRForm(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    version = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="Used in the URL.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="subforms"
    )

    class Meta:
        order_with_respect_to = "parent"


class FormInfoQuestion(models.Model):
    form = models.ForeignKey(
        MRForm, on_delete=models.CASCADE, related_name="info_questions"
    )
    text = models.CharField(max_length=200)
    link = models.URLField(max_length=200)


class FormInfoText(models.Model):
    form = models.ForeignKey(
        MRForm, on_delete=models.CASCADE, related_name="info_texts"
    )
    text = models.TextField()


# Questions
class BaseQuestion(models.Model):
    text = models.CharField(max_length=200)
    form = models.ForeignKey(MRForm, on_delete=models.CASCADE, related_name="questions")
    description = models.TextField(
        blank=True,
        help_text="Context about the question and its purpose, which will be shown to the user.",
    )
    required = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = "form"


class SelectQuestion(BaseQuestion):
    multiple = models.BooleanField(
        default=False,
        help_text="Allows multiple options to be selected if true.",
    )


class SelectOption(models.Model):
    label = models.CharField(max_length=200)
    default_selected = models.BooleanField(default=False)
    question = models.ForeignKey(
        SelectQuestion, on_delete=models.CASCADE, related_name="options"
    )


class TrueFalseQuestion(BaseQuestion):
    default_value = models.BooleanField(default=False)


class TextQuestion(BaseQuestion):
    placeholder = models.CharField(max_length=200, blank=True)
    lines = models.PositiveIntegerField(default=1)


class NumberQuestion(BaseQuestion):
    positive_only = models.BooleanField(default=False)


class DateQuestion(BaseQuestion):
    future_only = models.BooleanField(default=False)


class FileUploadQuestion(BaseQuestion):
    size_limit = models.PositiveIntegerField()
