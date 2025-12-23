"""AI content detection using HuggingFace transformers."""

from typing import Optional

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from post_automation.constants import MIN_TEXT_LENGTH_FOR_DETECTION
from post_automation.models.detection import DetectionResult
from post_automation.utils.config import get_settings
from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)


class AIDetector:
    """AI content detector using HuggingFace transformers."""

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize AI detector.

        Args:
            model_name: HuggingFace model name. If None, uses config default.
        """
        settings = get_settings()
        self.model_name = model_name or settings.hf_model_name
        self.hf_token = settings.hf_token

        logger.info(f"Initializing AI detector with model: {self.model_name}")

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.hf_token)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, token=self.hf_token
        )

        # Set to evaluation mode
        self.model.eval()

        logger.info("AI detector initialized successfully")

    def detect(self, text: str) -> DetectionResult:
        """
        Detect if text is AI-generated.

        Args:
            text: Text to analyze.

        Returns:
            Detection result with confidence score.
        """
        # Validate text length
        if len(text.strip()) < MIN_TEXT_LENGTH_FOR_DETECTION:
            logger.warning(
                f"Text length ({len(text.strip())}) is below minimum "
                f"({MIN_TEXT_LENGTH_FOR_DETECTION}). Results may be unreliable."
            )

        # Tokenize input
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512, padding=True
        )

        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)

        # Extract AI probability (assuming label 1 is AI)
        # Note: This may vary depending on the model. Adjust if needed.
        ai_probability = float(probabilities[0][1])

        is_ai = ai_probability > 0.5
        label = "AI" if is_ai else "Human"

        logger.info(
            f"Detection complete: {label} (confidence: {ai_probability:.2f}) "
            f"for text of length {len(text)}"
        )

        return DetectionResult(
            is_ai_generated=is_ai,
            confidence=ai_probability,
            label=label,
            model_name=self.model_name,
        )

    def detect_batch(self, texts: list[str]) -> list[DetectionResult]:
        """
        Detect AI content in multiple texts.

        Args:
            texts: List of texts to analyze.

        Returns:
            List of detection results.
        """
        logger.info(f"Running batch detection on {len(texts)} texts")
        results = []

        for text in texts:
            result = self.detect(text)
            results.append(result)

        return results


# Singleton instance (lazy-loaded)
_detector_instance: Optional[AIDetector] = None


def get_detector(model_name: Optional[str] = None) -> AIDetector:
    """
    Get singleton AI detector instance.

    Args:
        model_name: HuggingFace model name. If None, uses config default.

    Returns:
        AI detector instance.
    """
    global _detector_instance

    if _detector_instance is None:
        _detector_instance = AIDetector(model_name)

    return _detector_instance
