"""Data models for AI detection."""

from pydantic import BaseModel, Field


class DetectionResult(BaseModel):
    """Result of AI content detection."""

    is_ai_generated: bool = Field(..., description="Whether content is AI-generated")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)")
    label: str = Field(..., description="Classification label (AI or Human)")
    model_name: str = Field(..., description="Name of the model used for detection")

    class Config:
        json_schema_extra = {
            "example": {
                "is_ai_generated": True,
                "confidence": 0.87,
                "label": "AI",
                "model_name": "roberta-base-openai-detector",
            }
        }
