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


# Answers
class BaseAnswer(models.Model):
    # This means you can access true_false_answers with <user>.truefalseanswers etc.
    user = models.ForeignKey(
        user_model, on_delete=models.PROTECT, related_name="%(class)ss"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SelectAnswer(BaseAnswer):
    value = ArrayField(models.PositiveIntegerField(), blank=True, default=list)

    def get_selected_options(self) -> QuerySet[SelectOption]:
        return SelectOption.objects.filter(id__in=self.value)

    def set_selected_options(self, options: QuerySet[SelectOption]) -> None:
        self.value = list(options.values_list("id", flat=True))
        self.save()


class TrueFalseAnswer(BaseAnswer):
    value = models.BooleanField()


class TextAnswer(BaseAnswer):
    value = models.TextField()


class NumberAnswer(BaseAnswer):
    value = models.DecimalField(max_digits=10, decimal_places=2)


class DateAnswer(BaseAnswer):
    value = models.DateField()


class FileUploadAnswer(BaseAnswer):
    value = models.FileField(upload_to="answers/")


# QuestionAnswer models -- These should link to an 'Application' in the future.
class SelectQuestionAnswer(models.Model):
    question = models.ForeignKey(
        SelectQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        SelectAnswer, on_delete=models.CASCADE, related_name="question_answers"
    )


class TrueFalseQuestionAnswer(models.Model):
    question = models.ForeignKey(
        TrueFalseQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        TrueFalseAnswer, on_delete=models.CASCADE, related_name="question_answers"
    )


class TextQuestionAnswer(models.Model):
    question = models.ForeignKey(
        TextQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        TextAnswer, on_delete=models.CASCADE, related_name="question_answers"
    )


class NumberQuestionAnswer(models.Model):
    question = models.ForeignKey(
        NumberQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        NumberAnswer, on_delete=models.CASCADE, related_name="question_answers"
    )


class DateQuestionAnswer(models.Model):
    question = models.ForeignKey(
        DateQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        DateAnswer, on_delete=models.CASCADE, related_name="question_answers"
    )


class FileUploadQuestionAnswer(models.Model):
    question = models.ForeignKey(
        FileUploadQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.ForeignKey(
        FileUploadAnswer, on_delete=models.CASCADE, related_name="question_answers"
    )
