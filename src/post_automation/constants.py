"""Project-wide constants."""

# AI Detection thresholds
AI_CONFIDENCE_HIGH = 0.8
AI_CONFIDENCE_MEDIUM = 0.5

# Minimum text length for reliable AI detection (in characters)
MIN_TEXT_LENGTH_FOR_DETECTION = 50

# Default style configurations
DEFAULT_FONTS = ["Calibri", "Arial", "Times New Roman", "Verdana"]
DEFAULT_COLORS = {
    "primary": "#000000",
    "secondary": "#333333",
    "accent": "#0066CC",
}

# API Response messages
API_SUCCESS_MESSAGE = "Operation completed successfully"
API_ERROR_MESSAGE = "An error occurred"

# File type constants
PPTX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
PPT_MIME_TYPE = "application/vnd.ms-powerpoint"
