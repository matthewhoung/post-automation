"""Example tests to ensure pytest is working."""

import pytest


def test_example():
    """Example test."""
    assert 1 + 1 == 2


def test_sample_text_fixture(sample_text):
    """Test sample text fixture."""
    assert len(sample_text.strip()) > 0


def test_ai_generated_text_fixture(ai_generated_text):
    """Test AI-generated text fixture."""
    assert "utilize" in ai_generated_text.lower()
    assert "in order to" in ai_generated_text.lower()
