# Frontend (Dashboard & HITL UI)

## Scope

Per **specs/functional.md**, the frontend for Project Chimera consists of:

1. **Orchestrator Dashboard** – For Network Operators: monitor fleet health, view analytics, set campaign goals.
2. **HITL Review Interface** – For Human Reviewers: approve, edit, or reject escalated content (low-confidence or sensitive).

This repository focuses on **specifications, backend contracts, and agent runtime**. Frontend implementation will consume the same API contracts and schemas defined in `specs/technical.md`.

## Specification References

- **User stories:** `specs/functional.md` (§4 Action System, §6.2 HITL Review)
- **API contracts:** `specs/technical.md` (§2.3 Judge → HITL Review Queue Item, §2.4 MCP Tool `post_content`)
- **Data model:** `specs/technical.md` (§3 ER Diagram) – USER, REVIEW, POST, etc.

## Acceptance Criteria (from specs)

- Dashboard shows scheduled and recently published content; operators can intervene at a high level.
- HITL UI shows: content preview, confidence score, risk category, reason for escalation, and one-click Approve / Edit / Reject.
- All actions are traceable (tenant_id, agent_id, review decision) for audit.

## Implementation Notes

- Frontend can be implemented in a separate repo or `/frontend` directory, using the same `specs/` as source of truth.
- Auth and tenant context must align with multi-tenancy rules in `specs/_meta.md`.
- No frontend code is in this repository yet; this document defines the plan and acceptance criteria for evaluators.
