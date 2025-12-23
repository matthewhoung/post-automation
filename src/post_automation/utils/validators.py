"""Input validation utilities."""

from pathlib import Path

from post_automation.utils.config import get_settings


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


def validate_file_size(file_size: int) -> None:
    """
    Validate file size is within limits.

    Args:
        file_size: File size in bytes.

    Raises:
        ValidationError: If file size exceeds limit.
    """
    settings = get_settings()
    max_size = settings.max_upload_size_bytes

    if file_size > max_size:
        raise ValidationError(
            f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds "
            f"maximum allowed size ({settings.max_upload_size_mb}MB)"
        )


def validate_pptx_file(filename: str, file_size: int) -> None:
    """
    Validate PowerPoint file.

    Args:
        filename: Filename to validate.
        file_size: File size in bytes.

    Raises:
        ValidationError: If validation fails.
    """
    settings = get_settings()

    # Check extension
    ext = Path(filename).suffix.lower()
    if ext not in settings.allowed_extensions_list:
        raise ValidationError(
            f"Invalid file extension '{ext}'. "
            f"Allowed extensions: {', '.join(settings.allowed_extensions_list)}"
        )

    # Check size
    validate_file_size(file_size)


def validate_text_input(text: str, min_length: int = 10, max_length: int = 100000) -> None:
    """
    Validate text input.

    Args:
        text: Text to validate.
        min_length: Minimum text length.
        max_length: Maximum text length.

    Raises:
        ValidationError: If validation fails.
    """
    if not text or not text.strip():
        raise ValidationError("Text input cannot be empty")

    text_length = len(text.strip())

    if text_length < min_length:
        raise ValidationError(f"Text must be at least {min_length} characters long")

    if text_length > max_length:
        raise ValidationError(f"Text must not exceed {max_length} characters")
