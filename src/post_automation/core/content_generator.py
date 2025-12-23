"""Alternative content generation for AI-detected text."""

import re
from typing import Dict

from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentGenerator:
    """Generator for creating alternative content to replace AI-generated text."""

    def __init__(self):
        """Initialize content generator with simple rule-based transformations."""
        # Define simple word replacements for paraphrasing
        self.word_replacements: Dict[str, str] = {
            "utilize": "use",
            "in order to": "to",
            "due to the fact that": "because",
            "at this point in time": "now",
            "in the event that": "if",
            "for the purpose of": "to",
            "prior to": "before",
            "subsequent to": "after",
            "in close proximity to": "near",
            "is able to": "can",
            "has the ability to": "can",
            "in spite of": "despite",
            "on a regular basis": "regularly",
            "in the near future": "soon",
            "at the present time": "currently",
            "make a decision": "decide",
            "give consideration to": "consider",
            "make an assumption": "assume",
            "conduct an investigation": "investigate",
            "perform an analysis": "analyze",
        }

        logger.info("Content generator initialized with rule-based transformations")

    def generate(self, text: str) -> str:
        """
        Generate alternative content for AI-detected text.

        This uses simple rule-based transformations. For better quality,
        consider using a paraphrasing model like T5 or BART.

        Args:
            text: Original AI-generated text.

        Returns:
            Modified text.
        """
        logger.info(f"Generating alternative for text of length {len(text)}")

        modified_text = text

        # Apply word replacements
        for phrase, replacement in self.word_replacements.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            modified_text = pattern.sub(replacement, modified_text)

        # Simple sentence restructuring
        modified_text = self._simplify_sentences(modified_text)

        logger.info(f"Generated alternative text of length {len(modified_text)}")

        return modified_text

    def _simplify_sentences(self, text: str) -> str:
        """
        Apply simple sentence simplification rules.

        Args:
            text: Text to simplify.

        Returns:
            Simplified text.
        """
        # Remove excessive "that" usage
        text = re.sub(r"\bthat\s+that\b", "that", text, flags=re.IGNORECASE)

        # Simplify passive voice (basic patterns)
        text = re.sub(
            r"\bis being\s+(\w+ed)\b", r"is \1", text, flags=re.IGNORECASE
        )

        # Remove redundant "very" usage
        text = re.sub(r"\bvery\s+very\b", "very", text, flags=re.IGNORECASE)

        return text

    def generate_with_note(self, text: str) -> str:
        """
        Generate alternative content with a note that it was modified.

        Args:
            text: Original AI-generated text.

        Returns:
            Modified text with note.
        """
        modified = self.generate(text)
        return f"{modified}\n[Note: Content simplified for clarity]"


# Optional: Advanced paraphrasing with HuggingFace (commented out by default)
# Uncomment and install required models if you want to use transformer-based paraphrasing
"""
from transformers import pipeline

class TransformerContentGenerator:
    def __init__(self):
        self.paraphraser = pipeline(
            "text2text-generation",
            model="Vamsi/T5_Paraphrase_Paws"
        )

    def generate(self, text: str) -> str:
        # Limit text length for transformer
        if len(text) > 500:
            text = text[:500]

        result = self.paraphraser(
            f"paraphrase: {text}",
            max_length=len(text) * 2,
            num_return_sequences=1
        )

        return result[0]['generated_text']
"""
