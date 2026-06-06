from django.contrib import admin
from research.models.study import Study
from research.models.reviews import StatusChange
from form.models import UserFormSubmission


class StatusChangeInline(admin.TabularInline):
    """Inline admin for viewing status changes"""

    model = StatusChange
    extra = 0
    readonly_fields = ("status", "created_by", "created_at")
    can_delete = False
    fields = ("status", "created_by", "created_at")


class UserFormSubmissionInline(admin.TabularInline):
    """Inline admin for viewing form submissions"""

    model = UserFormSubmission
    readonly_fields = ("user", "form", "started_at", "updated_at")
    can_delete = False
    editable = False
    fields = ("user", "form", "started_at", "updated_at")
    verbose_name = "Form Submission"
    verbose_name_plural = "Form Submissions"

    def has_add_permission(self, request, obj=None):
        """Disable adding submissions from the inline"""
        return False


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("id", "study_name", "created_by", "created_at", "current_status")
    list_filter = ("created_at", "created_by")
    search_fields = ("id", "created_by__full_name", "created_by__email")
    readonly_fields = ("study_name", "created_at")
    inlines = [StatusChangeInline, UserFormSubmissionInline]

    def study_name(self, obj):
        return obj.name

    def current_status(self, obj):
        return obj.status

    def has_add_permission(self, request):
        """Disable adding studies through admin"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deleting studies through admin"""
        return False


@admin.register(StatusChange)
class StatusChangeAdmin(admin.ModelAdmin):
    list_display = ("id", "study", "status", "created_by", "created_at")
    list_filter = ("status", "created_at", "created_by")
    search_fields = ("study__id", "created_by__full_name")
    readonly_fields = ("created_at",)
    fields = ("study", "status", "created_by", "created_at")
