from django.contrib import admin
from django.db import models

from cdh.core.forms import TinyMCEWidget

from form.forms import StepAdminForm
from .models import (
    MRForm,
    Step,
    StepInfoText,
    BaseQuestion,
    SelectQuestion,
    SelectOption,
    TrueFalseQuestion,
    TextQuestion,
    NumberQuestion,
    DateQuestion,
    FileUploadQuestion,
    UserFormSubmission,
    QuestionResponse,
    StepCondition,
    QuestionCondition,
)

# Utils

class TinyMCETextFieldMixin:
    """
    A mixin for replacing all textfields with a TinyMCEWidget
    """

    class Media:
        js = (
            "cdh.core/js/jquery-3.6.1.min.js",
            "cdh.core/js/tinymce/tinymce.min.js",
            "cdh.core/js/tinymce/tinymce-jquery.min.js",
            "cdh.core/js/tinymce/shim.js",
        )

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCEWidget(
                plugins=[
                    "link",
                    "image",
                    "visualblocks",
                    "wordcount",
                    "lists",
                ]
            )
        },
    }


# Inline admins for related models
class StepInline(admin.StackedInline):
    model = Step
    extra = 0
    fields = ("name_nl", "name_en", "slug", "description_nl", "description_en")
    show_change_link = True
    fk_name = "form"


class SubstepInline(admin.StackedInline):
    model = Step
    extra = 0
    fields = ("name_nl", "name_en", "slug", "description_nl", "description_en")
    show_change_link = True
    fk_name = "parent"
    verbose_name = "Substep"
    verbose_name_plural = "Substeps"


class StepInfoTextInline(TinyMCETextFieldMixin, admin.StackedInline,):
    model = StepInfoText
    extra = 0
    fields = ("text_en", "text_nl")

class SelectOptionInline(admin.TabularInline):
    model = SelectOption
    extra = 0
    fields = ("label", "default_selected")


class StepConditionInline(admin.StackedInline):
    model = StepCondition
    extra = 0
    fk_name = "target_step"
    fields = (
        "condition_type",
        "trigger_question",
        "trigger_value",
        "repeat_count",
        "use_answer_as_count",
    )
    verbose_name = "Step Condition"
    verbose_name_plural = "Conditions Applied to This Step"


class QuestionConditionInline(admin.StackedInline):
    model = QuestionCondition
    extra = 0
    fk_name = "target_question"
    fields = (
        "condition_type",
        "trigger_question",
        "trigger_value",
        "repeat_count",
        "use_answer_as_count",
    )
    verbose_name = "Question Condition"
    verbose_name_plural = "Conditions Applied to This Question"


class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse.submissions.through
    extra = 0


class QuestionInline(admin.TabularInline):
    model = BaseQuestion
    extra = 0
    fields = ("id", "text", "required", "description")
    readonly_fields = ("id", "text", "required", "description")
    can_delete = False
    show_change_link = True
    verbose_name = "Question"
    verbose_name_plural = "Questions in This Step"

    def has_add_permission(self, request, obj=None):
        return False


# Main model admins
@admin.register(MRForm)
class MRFormAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [StepInline]


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = (
        "name_nl",
        "name_en",
        "slug",
        "form",
        "parent",
        "created_at_display",
    )
    list_filter = ("form", "parent")
    search_fields = ("name_nl", "name_en", "slug", "description_nl", "description_en")
    prepopulated_fields = {"slug": ("name_nl", "name_en")}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name_nl",
                    "name_en",
                    "slug",
                    "description_nl",
                    "description_en",
                )
            },
        ),
        (
            "Hierarchy",
            {
                "fields": ("form", "parent"),
                "description": "Set either 'form' (for top-level steps) OR 'parent' (for substeps), not both.",
            },
        ),
        (
            "Question Order",
            {
                "fields": ("question_order",),
                "description": "Set the display order of questions. Use the question IDs shown in the Questions inline below.",
            },
        ),
    )
    inlines = [
        SubstepInline,
        StepInfoTextInline,
        QuestionInline,
        StepConditionInline,
    ]
    form = StepAdminForm

    def created_at_display(self, obj):
        # Steps don't have created_at, but showing placeholder for structure
        return "-"

    created_at_display.short_description = "Info"



@admin.register(StepInfoText)
class StepInfoTextAdmin(TinyMCETextFieldMixin, admin.ModelAdmin,):
    list_display = ("short_text", "step")
    list_filter = ("step",)
    search_fields = ("text",)

    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = "Text"


# Question admins
@admin.register(SelectQuestion)
class SelectQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_nl", "text_en", "step", "required", "multiple")
    list_filter = ("step", "required", "multiple")
    search_fields = ("text_nl", "text_en", "description_nl", "description_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_nl",
                    "text_en",
                    "step",
                    "description_nl",
                    "description_en",
                    "required",
                )
            },
        ),
        ("Select Options", {"fields": ("multiple",)}),
    )
    inlines = [SelectOptionInline, QuestionConditionInline]


@admin.register(TrueFalseQuestion)
class TrueFalseQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_nl", "text_en", "step", "required", "default_value")
    list_filter = ("step", "required", "default_value")
    search_fields = ("text_nl", "text_en", "description_nl", "description_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_nl",
                    "text_en",
                    "step",
                    "description_nl",
                    "description_en",
                    "required",
                )
            },
        ),
        ("True/False Options", {"fields": ("default_value",)}),
    )
    inlines = [QuestionConditionInline]


@admin.register(TextQuestion)
class TextQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_nl", "text_en", "step", "required", "lines", "placeholder")
    list_filter = ("step", "required", "lines")
    search_fields = ("text_nl", "text_en", "description_nl", "description_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_nl",
                    "text_en",
                    "step",
                    "description_nl",
                    "description_en",
                    "required",
                )
            },
        ),
        ("Text Options", {"fields": ("placeholder", "lines")}),
    )
    inlines = [QuestionConditionInline]


@admin.register(NumberQuestion)
class NumberQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_nl", "text_en", "step", "required", "positive_only")
    list_filter = ("step", "required", "positive_only")
    search_fields = ("text_nl", "text_en", "description_nl", "description_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_nl",
                    "text_en",
                    "step",
                    "description_nl",
                    "description_en",
                    "required",
                )
            },
        ),
        ("Number Options", {"fields": ("positive_only",)}),
    )
    inlines = [QuestionConditionInline]


@admin.register(DateQuestion)
class DateQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_nl", "text_en", "step", "required", "future_only")
    list_filter = ("step", "required", "future_only")
    search_fields = ("text_nl", "text_en", "description_nl", "description_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_nl",
                    "text_en",
                    "step",
                    "description_nl",
                    "description_en",
                    "required",
                )
            },
        ),
        ("Date Options", {"fields": ("future_only",)}),
    )
    inlines = [QuestionConditionInline]


@admin.register(FileUploadQuestion)
class FileUploadQuestionAdmin(admin.ModelAdmin):
    list_display = ("text_nl", "text_en", "step", "required", "size_limit")
    list_filter = ("step", "required")
    search_fields = ("text_nl", "text_en", "description_nl", "description_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_nl",
                    "text_en",
                    "step",
                    "description_nl",
                    "description_en",
                    "required",
                )
            },
        ),
        ("File Upload Options", {"fields": ("size_limit",)}),
    )
    inlines = [QuestionConditionInline]


@admin.register(SelectOption)
class SelectOptionAdmin(admin.ModelAdmin):
    list_display = ("label_nl", "label_en", "question", "default_selected")
    list_filter = ("question", "default_selected")
    search_fields = ("label_nl", "label_en")


# User submission admins
@admin.register(UserFormSubmission)
class UserFormSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "form",
        "started_at",
        "updated_at",
        "completed_at",
        "is_complete",
    )
    list_filter = ("form", "completed_at", "started_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("started_at", "updated_at")
    inlines = [QuestionResponseInline]

    def is_complete(self, obj):
        return obj.completed_at is not None

    # Use boolean icon in admin list display
    is_complete.boolean = True

    # Adjust list display column name
    is_complete.short_description = "Completed"


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = (
        "first_submission",
        "question",
        "repeat_index",
        "answer_preview",
        "answered_at",
    )
    list_filter = ("answered_at",)
    search_fields = ("question__text",)
    readonly_fields = ("answered_at",)

    def answer_preview(self, obj):
        answer_str = str(obj.answer)
        return answer_str[:50] + "..." if len(answer_str) > 50 else answer_str

    answer_preview.short_description = "Answer"


TRIGGER_VALUE_HELP_TEXT = """
JSON field defining when this condition triggers. 
Examples: {"value": true}, {"value": "foo"}, {"option_ids": [1, 3]}, {"min": 5}. 
For a full explanation, see form/README.md.
"""


# Condition admins
@admin.register(StepCondition)
class StepConditionAdmin(admin.ModelAdmin):
    list_display = (
        "target_step",
        "condition_type",
        "trigger_question",
        "trigger_value_preview",
        "repeat_count",
    )
    list_filter = ("condition_type", "target_step__form")
    search_fields = ("target_step__name", "trigger_question__text")
    fieldsets = (
        (None, {"fields": ("target_step", "trigger_question", "condition_type")}),
        (
            "Trigger Configuration",
            {
                "fields": ("trigger_value",),
                "description": TRIGGER_VALUE_HELP_TEXT,
            },
        ),
        (
            "Repeat Configuration",
            {
                "fields": ("repeat_count", "use_answer_as_count"),
                "description": "For 'repeat' conditions: set repeat_count. For 'repeat_dynamic': check use_answer_as_count.",
            },
        ),
    )

    def trigger_value_preview(self, obj):
        value_str = str(obj.trigger_value)
        return value_str[:30] + "..." if len(value_str) > 30 else value_str

    trigger_value_preview.short_description = "Trigger Value"


@admin.register(QuestionCondition)
class QuestionConditionAdmin(admin.ModelAdmin):
    list_display = (
        "target_question",
        "condition_type",
        "trigger_question",
        "trigger_value_preview",
        "repeat_count",
    )
    list_filter = ("condition_type", "target_question__step__form")
    search_fields = ("target_question__text", "trigger_question__text")
    fieldsets = (
        (None, {"fields": ("target_question", "trigger_question", "condition_type")}),
        (
            "Trigger Configuration",
            {
                "fields": ("trigger_value",),
                "description": TRIGGER_VALUE_HELP_TEXT,
            },
        ),
        (
            "Repeat Configuration",
            {
                "fields": ("repeat_count", "use_answer_as_count"),
                "description": "For 'repeat' conditions: set repeat_count. For 'repeat_dynamic': check use_answer_as_count.",
            },
        ),
    )

    def trigger_value_preview(self, obj):
        value_str = str(obj.trigger_value)
        return value_str[:30] + "..." if len(value_str) > 30 else value_str

    trigger_value_preview.short_description = "Trigger Value"
