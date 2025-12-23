"""File handling utilities."""

import os
import uuid
from pathlib import Path
from typing import BinaryIO

from post_automation.utils.config import get_settings
from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)


def ensure_temp_dir() -> Path:
    """
    Ensure temporary directory exists.

    Returns:
        Path to temporary directory.
    """
    settings = get_settings()
    temp_dir = Path(settings.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def generate_temp_filename(extension: str = ".pptx") -> str:
    """
    Generate a unique temporary filename.

    Args:
        extension: File extension (default: .pptx).

    Returns:
        Full path to temporary file.
    """
    temp_dir = ensure_temp_dir()
    filename = f"{uuid.uuid4()}{extension}"
    return str(temp_dir / filename)


def save_uploaded_file(file_content: bytes, original_filename: str) -> str:
    """
    Save uploaded file to temporary directory.

    Args:
        file_content: File content as bytes.
        original_filename: Original filename.

    Returns:
        Path to saved file.
    """
    # Get file extension
    ext = Path(original_filename).suffix
    temp_path = generate_temp_filename(ext)

    # Save file
    with open(temp_path, "wb") as f:
        f.write(file_content)

    logger.info(f"Saved uploaded file to {temp_path}")
    return temp_path


def validate_file_extension(filename: str) -> bool:
    """
    Validate file has allowed extension.

    Args:
        filename: Filename to validate.

    Returns:
        True if extension is allowed, False otherwise.
    """
    settings = get_settings()
    ext = Path(filename).suffix.lower()
    return ext in settings.allowed_extensions_list


def cleanup_file(file_path: str) -> None:
    """
    Delete a file if it exists.

    Args:
        file_path: Path to file to delete.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup file {file_path}: {e}")
