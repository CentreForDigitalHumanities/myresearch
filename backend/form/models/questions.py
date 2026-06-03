from re import Pattern

from django.core.exceptions import ValidationError
from django.core.validators import validate_email, EmailValidator, RegexValidator
from django.db import models
from django.http import JsonResponse


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

    def clean(self) -> None:
        """Validate that questions are not attached to overview steps."""
        super().clean()
        if self.pk and self.step.is_overview:
            raise ValidationError(
                {"step": "Questions cannot be attached to overview steps."}
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

    class Meta:
        order_with_respect_to = "question"


class TrueFalseQuestion(BaseQuestion):
    default_value = models.BooleanField(default=False)


class TextQuestion(BaseQuestion):
    placeholder = models.CharField(max_length=200, blank=True)
    lines = models.PositiveIntegerField(default=1)
    is_email = models.BooleanField(default=False)

    def is_valid_email(self):
        temp_email = "hello@roordink.nl"
        validator = EmailValidator()
        validator(temp_email)

    @staticmethod
    def email_regex() -> str:
        validator = EmailValidator()
        full_pattern_string = validator.user_regex.pattern + "@" + validator.domain_regex.pattern
        return TextQuestion.convert_django_to_ts_regex(full_pattern_string)

        # "(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\\Z|^\"([\\001-\\010\\013\\014\\016-\\037!#-\\[\\]-\\177]|\\\\[\\001-\\011\\013\\014\\016-\\177])*\"\\Z)@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\\Z"
        #
        validator.message = "Enter a valid email address." # TODO: translation
        return validator.domain_regex

    @staticmethod
    def convert_django_to_ts_regex(django_regex_str: str) -> str:
        # 1. Replace \Z with $ # Python's \Z matches the end of the string. # JavaScript's $ matches the end of the string.
        import re

        ts_regex = django_regex_str.replace(r"\Z", "$")

        # 2. Convert octal escapes to hex escapes
        # Python regex often uses \000 format.
        # JS/TS requires \xHH format for hex.
        def octal_to_hex(match):
            octal_val = match.group(1)
            hex_val = hex(int(octal_val, 8))[2:].zfill(2)
            return f"\\x{hex_val}"

        # Regex to find \ followed by 3 octal digits
        ts_regex = re.sub(r"\\([0-7]{3})", octal_to_hex, ts_regex)
        return ts_regex


class NumberQuestion(BaseQuestion):
    positive_only = models.BooleanField(default=False)


class DateQuestion(BaseQuestion):
    future_only = models.BooleanField(default=False)


class FileUploadQuestion(BaseQuestion):
    size_limit = models.PositiveIntegerField()
