from django.db import models


class BaseQuestion(models.Model):
    text = models.CharField(max_length=200)
    step = models.ForeignKey(
        "form.Step", on_delete=models.CASCADE, related_name="questions"
    )
    description = models.TextField(
        blank=True,
        help_text="Context about the question and its purpose, which will be shown to the user.",
    )
    required = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = "step"

    @property
    def has_conditions(self) -> bool:
        """
        Returns True if there are any step or question conditions dependent on
        this question.
        """
        return (
            self.triggered_questioncondition.exists()  # type: ignore
            or self.triggered_stepcondition.exists()  # type: ignore
        )

    def get_subclass(self):
        """
        Returns the actual subclass instance (TextQuestion, SelectQuestion, etc.).
        BaseQuestion is used as a fallback.
        """
        for subclass_name in [
            "selectquestion",
            "truefalsequestion",
            "textquestion",
            "numberquestion",
            "datequestion",
            "fileuploadquestion",
        ]:
            if hasattr(self, subclass_name):
                return getattr(self, subclass_name)
        return self

    def __str__(self):
        return f"{self.text} ({self.pk})"


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
