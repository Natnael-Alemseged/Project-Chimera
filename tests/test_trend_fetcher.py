"""
Test suite for trend detection/fetching functionality.

Tests the expected output structure per SRS FR 2.2 (Trend Detection) and
specs/technical.md. These tests intentionally fail until the implementation
is added (TDD approach).
"""

import pytest
from pydantic import BaseModel, ValidationError, Field


# Pydantic model for trend alert output contract
class TrendAlertOutput(BaseModel):
    """Expected output structure for trend detection (FR 2.2)."""
    trend_alert: bool
    topics: list[str]
    relevance_score: float = Field(ge=0.0, le=1.0)  # 0.0 to 1.0
    alert_message: str


# This import will fail until the module is implemented
# Per specs/technical.md and skills/trend_detection_alerting/README.md
try:
    from skills.trend_detection_alerting import fetch_and_filter_trends
except ImportError:
    # Expected failure - module doesn't exist yet
    fetch_and_filter_trends = None


def test_trend_data_structure():
    """
    Test that fetch_and_filter_trends returns the expected structure.

    Per SRS FR 2.2: Trend Detection should emit structured alerts with
    topics, relevance scores, and alert messages.
    """
    # This will fail with ModuleNotFoundError until implementation exists
    assert fetch_and_filter_trends is not None, (
        "Module skills.trend_detection_alerting.fetch_and_filter_trends "
        "must be implemented"
    )

    # Example input per skills/trend_detection_alerting/README.md
    input_data = {
        "tenant_id": "tenant-xyz",
        "agent_id": "agent-ethiopia-fashion-001",
        "window_hours": 4,
        "resources": [
            "news://ethiopia/fashion/trends",
            "twitter://mentions/recent"
        ],
        "min_cluster_score": 0.75,
        "max_trends": 10,
        "now": "2026-02-06T10:00:00Z"
    }

    # Call the function (will fail until implemented)
    result = fetch_and_filter_trends(**input_data)

    # Validate structure matches contract
    assert isinstance(result, dict), "Result must be a dictionary"

    # Expected keys per contract
    required_keys = ["trend_alert", "topics", "relevance_score", "alert_message"]
    for key in required_keys:
        assert key in result, f"Result must contain key '{key}'"

    # Validate types
    assert isinstance(result["trend_alert"], bool), "trend_alert must be bool"
    assert isinstance(result["topics"], list), "topics must be a list"
    assert all(isinstance(topic, str) for topic in result["topics"]), (
        "All topics must be strings"
    )
    assert isinstance(result["relevance_score"], float), (
        "relevance_score must be a float"
    )
    assert 0.0 <= result["relevance_score"] <= 1.0, (
        "relevance_score must be between 0.0 and 1.0"
    )
    assert isinstance(result["alert_message"], str), (
        "alert_message must be a string"
    )


def test_trend_alert_pydantic_validation():
    """
    Test that trend alert output can be validated with Pydantic.

    Uses the TrendAlertOutput model to ensure strict contract compliance.
    """
    # Example valid output structure
    example_output = {
        "trend_alert": True,
        "topics": ["ethiopian-summer-streetwear", "africa-fashion"],
        "relevance_score": 0.92,
        "alert_message": "Emerging trend detected: Ethiopian summer streetwear gaining traction"
    }

    # Should validate successfully
    validated = TrendAlertOutput(**example_output)
    assert validated.trend_alert is True
    assert len(validated.topics) == 2
    assert validated.relevance_score == 0.92

    # Invalid example (relevance_score out of range)
    invalid_output = {
        "trend_alert": True,
        "topics": ["test"],
        "relevance_score": 1.5,  # Invalid: > 1.0
        "alert_message": "Test"
    }

    # Should raise ValidationError
    with pytest.raises(ValidationError):
        TrendAlertOutput(**invalid_output)


def test_trend_fetcher_with_example_data():
    """
    Test trend fetcher with concrete example data matching contract.

    Per specs/technical.md: trend data should include topics, scores, and
    structured metadata.
    """
    # This will fail until fetch_and_filter_trends is implemented
    assert fetch_and_filter_trends is not None

    input_data = {
        "tenant_id": "tenant-xyz",
        "agent_id": "agent-ethiopia-fashion-001",
        "window_hours": 4,
        "resources": ["news://ethiopia/fashion/trends"],
        "min_cluster_score": 0.75,
        "max_trends": 5,
        "now": "2026-02-06T10:00:00Z"
    }

    result = fetch_and_filter_trends(**input_data)

    # Expected structure per contract
    expected_structure = {
        "trend_alert": bool,
        "topics": list,
        "relevance_score": float,
        "alert_message": str
    }

    for key, expected_type in expected_structure.items():
        assert key in result, f"Missing key: {key}"
        assert isinstance(result[key], expected_type), (
            f"Key '{key}' must be of type {expected_type.__name__}"
        )
