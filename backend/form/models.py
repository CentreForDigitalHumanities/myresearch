from django.db import models
from django.db.models import QuerySet, Q
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

user_model = get_user_model()


class FormConfig(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Form(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    config = models.OneToOneField(
        FormConfig, on_delete=models.CASCADE, related_name="form"
    )


# Step and StepInfo
class Step(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="Used in the URL.",
    )

    form = models.ForeignKey(
        Form, null=True, blank=True, on_delete=models.CASCADE, related_name="steps"
    )
    form_order = models.PositiveIntegerField(
        null=True, blank=True, help_text="The order of this step within the form."
    )

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="substeps"
    )
    parent_order = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="The order of this step within its parent step.",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(parent_order__isnull=False, form_order__isnull=True)
                | Q(parent_order__isnull=True, form_order__isnull=False),
                name="either_form_order_or_parent_order",
            )
        ]


class StepInfo(models.Model):
    """
    More information and FAQ for a specific Step within a Form.
    """

    step = models.OneToOneField(
        Step, null=True, blank=True, on_delete=models.CASCADE, related_name="info"
    )


class StepInfoQuestion(models.Model):
    step_info = models.ForeignKey(
        StepInfo, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=200)
    link = models.URLField(max_length=200)


class StepInfoText(models.Model):
    step_info = models.ForeignKey(
        StepInfo, on_delete=models.CASCADE, related_name="texts"
    )
    text = models.TextField()


# Questions
class BaseQuestion(models.Model):
    text = models.CharField(max_length=200)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    description = models.TextField(
        blank=True,
        help_text="Context about the question and its purpose, which will be shown to the user.",
    )
    required = models.BooleanField(default=False)

    class Meta:
        abstract = True


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
        user_model, on_delete=models.CASCADE, related_name="%(class)ss"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
