from django.core.exceptions import ValidationError
from django.conf import settings


def validate_slug_not_overview(value: str) -> None:
    """
    Make sure the slug is not the same as the overview slug, which is reserved.
    """
    overview_slug = settings.OVERVIEW_STEP_SLUG.lower()

    if value.lower() == overview_slug:
        raise ValidationError(
            f"The slug '{overview_slug}' is reserved and cannot be used."
        )
