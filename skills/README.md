# Project Chimera – Skills Overview

Runtime skills are **capability packages** that Chimera’s FastRender Swarm (Planner / Workers / Judges) call to perform complex operations in a consistent, spec‑aligned way.

- Skills are called primarily by **Workers**, sometimes coordinated by **Planners** and validated by **Judges**.
- Each skill:
  - Wraps one or more **MCP Tools/Resources**.
  - Exposes a clear **JSON input/output contract**.
  - Enforces **policy and safety rules** (HITL, budgets, persona constraints).
- Skills do **not** bypass MCP or talk directly to external APIs.

This directory currently defines three critical skills:

1. `trend_detection_alerting` – Perception: detect and emit “Trend Alerts”.
2. `multimodal_content_generation` – Creative engine: orchestrate text, image, and video.
3. `autonomous_transaction` – Agentic commerce: budget‑aware on‑chain operations.

Refer to each subfolder README for detailed contracts.

