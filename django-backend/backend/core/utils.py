import re

from django.core.exceptions import ValidationError


def validate_google_user_id(value):
    """Validate the given value is either empty, None, or 21 digits.

    Raises:
        ValidationError: if Google user ID is invalid.
    """
    if value and not re.match(r"^\d{21}$", value):
        raise ValidationError("Google user ID should be 21 digits.")
