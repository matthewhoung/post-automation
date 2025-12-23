"""Pytest configuration and fixtures."""

import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    """Get test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_text():
    """Sample text for testing."""
    return """
    The quick brown fox jumps over the lazy dog. This is a sample text for testing
    AI detection capabilities. It should be long enough to provide meaningful results.
    """


@pytest.fixture(scope="session")
def ai_generated_text():
    """Sample AI-generated text."""
    return """
    In order to utilize the capabilities of the system, one must first understand
    the fundamental principles that govern its operation. Due to the fact that
    the implementation is complex, it is necessary to conduct a thorough analysis.
    """


@pytest.fixture
def mock_env(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("HF_TOKEN", "test_token")
    monkeypatch.setenv("HF_MODEL_NAME", "test-model")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
