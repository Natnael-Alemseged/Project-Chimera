#!/usr/bin/env python3
"""
Project Chimera – Small demo to demonstrate contract validation and Judge/HITL logic.

This script shows:
  1. Trend alert output contract validation (per specs/technical.md, skills/trend_detection_alerting)
  2. Judge decision simulation: Auto-Approve vs HITL vs Reject (per specs/_meta.md, architecture)
  3. No real MCP or backend – only structure and rules.
"""

from pydantic import BaseModel, Field, ValidationError

# --- Contract: Trend Alert Output (FR 2.2) ---
class TrendAlertOutput(BaseModel):
    trend_alert: bool
    topics: list[str]
    relevance_score: float = Field(ge=0.0, le=1.0)
    alert_message: str


# --- Judge decision (per specs: confidence thresholds) ---
def judge_decision(confidence: float, risk_category: str) -> str:
    """Simulate Judge routing: Auto-Approve, HITL, or Reject."""
    if confidence >= 0.90 and "high" not in risk_category.lower():
        return "AUTO_APPROVE"
    if confidence >= 0.70:
        return "HITL_REVIEW"
    return "REJECT"


def main() -> None:
    print("=" * 60)
    print("  Project Chimera – Demo (contracts + Judge logic)")
    print("=" * 60)

    # 1. Validate trend alert contract
    print("\n1. Trend Alert Contract (FR 2.2)")
    sample_trend = {
        "trend_alert": True,
        "topics": ["ethiopian-summer-streetwear", "africa-fashion"],
        "relevance_score": 0.92,
        "alert_message": "Emerging trend: Ethiopian summer streetwear gaining traction",
    }
    out = TrendAlertOutput(**sample_trend)
    print(f"   Valid structure: trend_alert={out.trend_alert}, topics={out.topics[:2]}, score={out.relevance_score}")
    print("   ✅ Contract validated.")

    # 2. Reject invalid (relevance_score > 1)
    print("\n2. Invalid payload (relevance_score > 1.0)")
    try:
        TrendAlertOutput(**{**sample_trend, "relevance_score": 1.5})
    except ValidationError as e:
        print("   ✅ Correctly rejected:", e.errors()[0]["msg"][:50] + "...")

    # 3. Judge simulation
    print("\n3. Judge decision simulation (per specs)")
    cases = [
        (0.92, "low"),
        (0.78, "brand_safety_medium"),
        (0.65, "high"),
    ]
    for conf, risk in cases:
        decision = judge_decision(conf, risk)
        print(f"   confidence={conf}, risk={risk} → {decision}")

    print("\n" + "=" * 60)
    print("  Demo complete. Contracts and Judge logic align with specs/.")
    print("=" * 60)


if __name__ == "__main__":
    main()
