"""API request/response schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class TextDetectionRequest(BaseModel):
    """Request schema for text detection."""

    text: str = Field(..., min_length=10, description="Text to analyze")
    model: Optional[str] = Field(
        default="roberta-base-openai-detector", description="Model name to use"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "text": "The quick brown fox jumps over the lazy dog in a systematic manner.",
                "model": "roberta-base-openai-detector",
            }
        }


class ModifyPPTXRequest(BaseModel):
    """Request schema for PowerPoint modification."""

    replace_ai_content: bool = Field(default=True, description="Replace AI-detected content")
    font_name: Optional[str] = Field(None, description="Font name to apply")
    text_color: Optional[str] = Field(None, description="Text color (hex format)")
    confidence_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="AI confidence threshold for replacement"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "replace_ai_content": True,
                "font_name": "Arial",
                "text_color": "#000000",
                "confidence_threshold": 0.7,
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Timestamp (ISO format)")
    version: str = Field(..., description="Application version")
    models_loaded: bool = Field(..., description="Whether AI models are loaded")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-12-23T10:30:00Z",
                "version": "0.1.0",
                "models_loaded": True,
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Error type")
    timestamp: str = Field(..., description="Timestamp (ISO format)")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "File size exceeds maximum allowed size",
                "error_type": "ValidationError",
                "timestamp": "2025-12-23T10:30:00Z",
            }
        }
