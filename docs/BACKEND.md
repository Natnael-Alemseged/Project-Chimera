# Backend (Agent Runtime, MCP & Data)

## Scope

Per **specs/functional.md** and **specs/technical.md**, the backend for Project Chimera consists of:

1. **Agent runtime** – FastRender Swarm: Planner (decompose goals → task DAG), Workers (execute atomic tasks via MCP Tools), Judge (validate with OCC, confidence scoring, HITL escalation).
2. **MCP integration layer** – All external IO via MCP Resources and Tools (no direct API calls). Servers for Twitter, Weaviate, Coinbase, news, etc., as in `specs/technical.md` §4.
3. **Skills** – Runtime capability packages that wrap MCP: `trend_detection_alerting`, `multimodal_content_generation`, `autonomous_transaction` (contracts in `skills/*/README.md`).
4. **Data layer** – PostgreSQL (transactional), Weaviate (semantic memory), Redis (episodic cache, task queues). Schema and ERD in `specs/technical.md` §3.
5. **Governance** – Resource Governor / CFO Judge for budget checks; HITL review queue fed by Judge decisions.

This repository holds **backend specifications, contracts, and structure** (e.g. `pyproject.toml`, `tests/`, `skills/` contracts, `scripts/demo_chimera.py`). Full backend implementation will satisfy the same contracts and specs.

## Specification References

- **API contracts:** `specs/technical.md` (§2 Task payload, Artifact, HITL Review item, `post_content`, `send_transaction`)
- **Data model:** `specs/technical.md` (§3 ERD, hybrid storage, Weaviate Memory schema)
- **MCP topology:** `specs/technical.md` (§4 MCP Host, core servers)
- **User stories:** `specs/functional.md` (Cognitive Core, Perception, Creative Engine, Action, Agentic Commerce, Orchestration)
- **Constitutional rules:** `specs/_meta.md` (MCP-only IO, FastRender only, HITL, budget governance)
- **Skill I/O:** `skills/trend_detection_alerting/README.md`, `skills/multimodal_content_generation/README.md`, `skills/autonomous_transaction/README.md`

## Acceptance Criteria (from specs)

- Planner produces task DAGs; Workers consume tasks and call MCP Tools only; Judge validates artifacts and routes to Approve / HITL / Reject by confidence and risk.
- All external access (social, DB, wallet) goes through MCP; no direct Twitter/Weaviate/Coinbase calls in business logic.
- Data access is tenant-scoped (`tenant_id`); Postgres + Weaviate + Redis used as per technical spec.
- Budget guards and CFO Judge applied to every transaction path; non-custodial wallets only (Coinbase AgentKit).

## Implementation Notes

- Backend implementation can live in this repo (e.g. `src/` or package layout) or a separate service repo, using `specs/` and `skills/` as source of truth.
- **Tests** in `tests/` define contracts (TDD); implementations should be written to pass those tests.
- **Demo:** `scripts/demo_chimera.py` shows contract validation and Judge decision logic; no real MCP or DB required.
- No full backend server or worker processes are implemented yet; this document defines the backend scope and acceptance criteria for evaluators.
