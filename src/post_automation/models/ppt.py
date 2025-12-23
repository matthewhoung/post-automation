"""Data models for PowerPoint operations."""

from typing import List, Optional

from pydantic import BaseModel, Field

from post_automation.models.detection import DetectionResult


class SlideText(BaseModel):
    """Text extracted from a PowerPoint slide."""

    slide_number: int = Field(..., ge=0, description="Slide number (0-indexed)")
    text: str = Field(..., description="Extracted text content")
    shape_count: int = Field(..., ge=0, description="Number of shapes in the slide")

    class Config:
        json_schema_extra = {
            "example": {
                "slide_number": 0,
                "text": "Introduction to Machine Learning",
                "shape_count": 3,
            }
        }


class SlideDetection(BaseModel):
    """AI detection result for a single slide."""

    slide_number: int = Field(..., ge=0, description="Slide number (0-indexed)")
    text: str = Field(..., description="Slide text content")
    detection: DetectionResult = Field(..., description="Detection result")

    class Config:
        json_schema_extra = {
            "example": {
                "slide_number": 0,
                "text": "Introduction to Machine Learning",
                "detection": {
                    "is_ai_generated": True,
                    "confidence": 0.92,
                    "label": "AI",
                    "model_name": "roberta-base-openai-detector",
                },
            }
        }


class PresentationDetection(BaseModel):
    """AI detection results for an entire presentation."""

    file_name: str = Field(..., description="Original filename")
    total_slides: int = Field(..., ge=0, description="Total number of slides")
    ai_slides: int = Field(..., ge=0, description="Number of AI-generated slides")
    human_slides: int = Field(..., ge=0, description="Number of human-written slides")
    slides: List[SlideDetection] = Field(..., description="Per-slide detection results")

    class Config:
        json_schema_extra = {
            "example": {
                "file_name": "presentation.pptx",
                "total_slides": 10,
                "ai_slides": 6,
                "human_slides": 4,
                "slides": [],
            }
        }


class Replacement(BaseModel):
    """Text replacement instruction for PowerPoint."""

    slide_num: int = Field(..., ge=0, description="Slide number (0-indexed)")
    old_text: str = Field(..., description="Text to replace")
    new_text: str = Field(..., description="Replacement text")

    class Config:
        json_schema_extra = {
            "example": {
                "slide_num": 0,
                "old_text": "AI-generated content here",
                "new_text": "Human-written alternative",
            }
        }


class ColorScheme(BaseModel):
    """Color scheme for PowerPoint styling."""

    text_color: Optional[str] = Field(None, description="Text color (hex format)")
    background_color: Optional[str] = Field(None, description="Background color (hex format)")

    class Config:
        json_schema_extra = {"example": {"text_color": "#000000", "background_color": "#FFFFFF"}}


class StyleConfig(BaseModel):
    """Style configuration for PowerPoint modification."""

    font_name: Optional[str] = Field(None, description="Font name")
    font_size: Optional[int] = Field(None, ge=8, le=72, description="Font size (8-72)")
    color_scheme: Optional[ColorScheme] = Field(None, description="Color scheme")

    class Config:
        json_schema_extra = {
            "example": {
                "font_name": "Arial",
                "font_size": 18,
                "color_scheme": {"text_color": "#000000"},
            }
        }
