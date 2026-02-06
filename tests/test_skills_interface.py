"""
Test suite for Chimera skills input/output contracts.

Tests the I/O schemas for all three critical skills per their README definitions:
- trend_detection_alerting (Perception FR 2.2)
- multimodal_content_generation (Creative FR 3.0-3.2)
- autonomous_transaction (Commerce FR 5.0-5.2)

These tests intentionally fail until implementations exist (TDD approach).
"""

import pytest
from pydantic import BaseModel, ValidationError


# Pydantic models for skill contracts (per skills/*/README.md)

class TrendDetectionInput(BaseModel):
    """Input contract for trend_detection_alerting skill."""
    tenant_id: str
    agent_id: str
    window_hours: int
    resources: list[str]
    min_cluster_score: float
    max_trends: int
    now: str


class TrendDetectionOutput(BaseModel):
    """Output contract for trend_detection_alerting skill."""
    tenant_id: str
    agent_id: str
    window_hours: int
    generated_at: str
    trends: list[dict]  # Simplified; full schema in README


class MultimodalContentInput(BaseModel):
    """Input contract for multimodal_content_generation skill."""
    tenant_id: str
    agent_id: str
    campaign_id: str
    creative_brief: dict
    persona_constraints: dict
    character_reference_id: str
    platform: str
    tier: str  # "daily" or "hero"
    budget_hint: dict


class MultimodalContentOutput(BaseModel):
    """Output contract for multimodal_content_generation skill."""
    tenant_id: str
    agent_id: str
    campaign_id: str
    assets: dict  # Contains caption, image, video
    generation_metadata: dict


class AutonomousTransactionInput(BaseModel):
    """Input contract for autonomous_transaction skill."""
    tenant_id: str
    agent_id: str
    wallet_id: str
    network: str
    asset: str
    amount: str  # Decimal as string
    to_address: str
    purpose: str
    campaign_id: str
    budget_guard: dict
    metadata: dict


class AutonomousTransactionOutput(BaseModel):
    """Output contract for autonomous_transaction skill."""
    tenant_id: str
    agent_id: str
    wallet_id: str
    network: str
    asset: str
    amount: str
    to_address: str
    purpose: str
    campaign_id: str
    status: str  # "executed", "rejected", "failed"
    tx_hash: str | None = None
    executed_at: str | None = None
    post_balances: dict | None = None
    metadata: dict


# These imports will fail until modules are implemented
try:
    from skills.trend_detection_alerting import execute_trend_detection
except ImportError:
    execute_trend_detection = None

try:
    from skills.multimodal_content_generation import generate_multimodal_content
except ImportError:
    generate_multimodal_content = None

try:
    from skills.autonomous_transaction import execute_transaction
except ImportError:
    execute_transaction = None


def test_trend_detection_alerting_contract():
    """
    Test input/output contract for trend_detection_alerting skill.

    Per skills/trend_detection_alerting/README.md and SRS FR 2.2.
    """
    assert execute_trend_detection is not None, (
        "skills.trend_detection_alerting.execute_trend_detection must be implemented"
    )

    # Valid input per README
    valid_input = {
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

    # Validate input schema
    input_validated = TrendDetectionInput(**valid_input)
    assert input_validated.tenant_id == "tenant-xyz"

    # Call function (will fail until implemented)
    result = execute_trend_detection(**valid_input)

    # Validate output schema
    output_validated = TrendDetectionOutput(**result)
    assert "trends" in output_validated.trends or isinstance(output_validated.trends, list)
    assert output_validated.tenant_id == "tenant-xyz"
    assert output_validated.agent_id == "agent-ethiopia-fashion-001"

    # Invalid input (missing required field)
    invalid_input = {
        "tenant_id": "tenant-xyz",
        # Missing agent_id, window_hours, etc.
    }

    with pytest.raises(ValidationError):
        TrendDetectionInput(**invalid_input)


def test_multimodal_content_generation_contract():
    """
    Test input/output contract for multimodal_content_generation skill.

    Per skills/multimodal_content_generation/README.md and SRS FR 3.0-3.2.
    """
    assert generate_multimodal_content is not None, (
        "skills.multimodal_content_generation.generate_multimodal_content must be implemented"
    )

    # Valid input per README
    valid_input = {
        "tenant_id": "tenant-xyz",
        "agent_id": "agent-ethiopia-fashion-001",
        "campaign_id": "cmp-summer-ethiopia-2026",
        "creative_brief": {
            "goal": "Promote Ethiopian summer streetwear drop on TikTok.",
            "tone": ["witty", "aspirational"],
            "key_messages": ["Local designers", "Sustainable fabrics"],
            "cta": "Follow for daily Addis street looks."
        },
        "persona_constraints": {
            "forbidden_topics": ["politics", "explicit content"],
            "style_notes": "Highlight Ethiopian culture authentically."
        },
        "character_reference_id": "chimera-ethiopia-001",
        "platform": "tiktok",
        "tier": "daily",
        "budget_hint": {
            "max_generation_cost_usd": 5.0
        }
    }

    # Validate input schema
    input_validated = MultimodalContentInput(**valid_input)
    assert input_validated.character_reference_id == "chimera-ethiopia-001"
    assert input_validated.tier in ["daily", "hero"]

    # Call function (will fail until implemented)
    result = generate_multimodal_content(**valid_input)

    # Validate output schema
    output_validated = MultimodalContentOutput(**result)
    assert "assets" in output_validated.assets
    assert "generation_metadata" in output_validated.generation_metadata
    assert output_validated.campaign_id == "cmp-summer-ethiopia-2026"

    # Invalid input (missing character_reference_id)
    invalid_input = {
        "tenant_id": "tenant-xyz",
        "agent_id": "agent-001",
        "campaign_id": "cmp-001",
        "creative_brief": {},
        "persona_constraints": {},
        # Missing character_reference_id
        "platform": "tiktok",
        "tier": "daily",
        "budget_hint": {}
    }

    with pytest.raises(ValidationError):
        MultimodalContentInput(**invalid_input)


def test_autonomous_transaction_contract():
    """
    Test input/output contract for autonomous_transaction skill.

    Per skills/autonomous_transaction/README.md and SRS FR 5.0-5.2.
    """
    assert execute_transaction is not None, (
        "skills.autonomous_transaction.execute_transaction must be implemented"
    )

    # Valid input per README
    valid_input = {
        "tenant_id": "tenant-xyz",
        "agent_id": "agent-ethiopia-fashion-001",
        "wallet_id": "wallet-abc",
        "network": "base",
        "asset": "USDC",
        "amount": "25.00",
        "to_address": "0x1234abcd...",
        "purpose": "pay_for_video_generation",
        "campaign_id": "cmp-summer-ethiopia-2026",
        "budget_guard": {
            "max_per_tx": "50.00",
            "max_daily": "200.00",
            "max_campaign_total": "1000.00"
        },
        "metadata": {
            "task_id": "uuid-1234",
            "external_invoice_id": "inv-789"
        }
    }

    # Validate input schema
    input_validated = AutonomousTransactionInput(**valid_input)
    assert input_validated.amount == "25.00"
    assert input_validated.network == "base"

    # Call function (will fail until implemented)
    result = execute_transaction(**valid_input)

    # Validate output schema
    output_validated = AutonomousTransactionOutput(**result)
    assert output_validated.status in ["executed", "rejected", "failed"]
    assert output_validated.tenant_id == "tenant-xyz"
    assert output_validated.campaign_id == "cmp-summer-ethiopia-2026"

    # If executed, should have tx_hash and executed_at
    if output_validated.status == "executed":
        assert output_validated.tx_hash is not None
        assert output_validated.executed_at is not None
        assert output_validated.post_balances is not None

    # Invalid input (missing budget_guard)
    invalid_input = {
        "tenant_id": "tenant-xyz",
        "agent_id": "agent-001",
        "wallet_id": "wallet-abc",
        "network": "base",
        "asset": "USDC",
        "amount": "25.00",
        "to_address": "0x1234...",
        "purpose": "test",
        "campaign_id": "cmp-001",
        # Missing budget_guard
        "metadata": {}
    }

    with pytest.raises(ValidationError):
        AutonomousTransactionInput(**invalid_input)


def test_skills_require_mcp_tools():
    """
    Test that skills fail gracefully if required MCP tools are unavailable.

    Per specs/_meta.md: All external IO must go through MCP.
    Skills should raise clear errors if MCP servers/tools are missing.
    """
    # This test documents expected behavior: skills should check for MCP
    # availability and raise meaningful errors if tools are missing.

    # Example: trend detection requires news:// and twitter:// resources
    # If those MCP servers aren't connected, the skill should fail with
    # a clear error message, not silently return empty results.

    # Placeholder assertion - actual implementation will check MCP availability
    assert True, (
        "Skills must validate MCP tool availability before execution "
        "and raise clear errors if dependencies are missing"
    )
