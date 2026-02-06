# Project Chimera – Master Specification Meta

## 1. Purpose and Strategic Scope

Project Chimera is an **Autonomous Influencer Network** that turns static content schedulers into **persistent, goal-directed digital agents** with:

- **Perception** – continuous ingestion of social, news, and market signals.
- **Reasoning** – hierarchical swarm cognition (Planner / Worker / Judge).
- **Creative expression** – multimodal content generation (text, image, video).
- **Economic agency** – non-custodial wallets and on-chain transactions.

Per SRS §1.1–1.3, the system supports a **fleet of Chimera Agents** operated under a **Single-Orchestrator Model**: one human Super-Orchestrator commands a hierarchy of Manager Agents and Worker Swarms that can scale to **thousands of virtual influencers**.

This `_meta` spec defines the **constitution** of the project: high-level vision, scope, and non‑negotiable rules that govern all downstream specs and implementations.

---

## 2. Strategic Model and Business Scope

### 2.1 Single-Orchestrator Operational Model (SRS §1.2)

The system follows a **Fractal Orchestration** pattern:

- **Super-Orchestrator (human)** – defines portfolio-level strategy, risk bounds, and policies.
- **Manager Agents** – manage specific niches/brands (e.g., Ethiopian fashion, crypto education).
- **Worker Swarms** – ephemeral sub-processes (FastRender roles) executing concrete tasks.

Escalation follows **Management by Exception**:

- Routine errors are handled by self-healing workflows.
- Edge cases and high-risk scenarios escalate to humans (HITL Reviewers, Network Operators).

### 2.2 Business Models (SRS §1.3)

Chimera supports three primary business models:

1. **Digital Talent Agency Model**
   - AiQEM operates and monetizes in-house AI influencers.
   - Revenue via ads, sponsorships, affiliate sales.

2. **Platform-as-a-Service (PaaS) Model**
   - External brands lease “Chimera OS” to run their own virtual influencers.
   - Strict multi-tenancy and data isolation.

3. **Hybrid Ecosystem Model**
   - Combination of in-house flagship agents plus a 3rd-party developer ecosystem.
   - Agents become **economic entities** using Agentic Commerce:
     - Each agent has a non-custodial wallet (Coinbase AgentKit).
     - Agents can receive payments, pay for resources, and manage P&L.

---

## 3. Core Architectural Patterns

### 3.1 FastRender Swarm (SRS §3.1)

Chimera rejects monolithic agents and uses **Hierarchical Swarm** with roles:

- **Planner** – maintains global campaign goals and state, decomposes into a **task DAG**, performs dynamic re-planning on context shifts.
- **Worker** – stateless executor of atomic tasks (generate caption, call image tool, schedule post).
- **Judge** – governance and QA layer; validates outputs, enforces persona/safety constraints, and uses **Optimistic Concurrency Control (OCC)** for state consistency.

### 3.2 Model Context Protocol (MCP) (SRS §3.2)

All external IO goes through **MCP**:

- **Resources** – passive data streams (mentions, news, market prices).
- **Tools** – executable actions (post content, generate image, send transaction).
- **Prompts** – reusable structured reasoning templates.

MCP is the “**USB-C for AI**” that ensures agents are insulated from API volatility.

### 3.3 Agentic Commerce (SRS §1.3, §4.x)

Each agent can:

- Hold a **non-custodial wallet** via Coinbase AgentKit.
- Execute on-chain transactions (receive payments, pay for compute/tools).
- Maintain per-agent budgets and P&L.

---

## 4. Key Definitions (Glossary)

From SRS §1.4:

- **Chimera Agent** – a sovereign digital persona with:
  - SOUL.md‑defined backstory, voice, values, and directives.
  - Hierarchical memory (short-term cache, long-term semantic memories).
  - Non-custodial wallet for economic actions.

- **Orchestrator** – central control plane responsible for:
  - Fleet-level strategy and resource allocation.
  - Multi-tenant isolation and governance.
  - Providing dashboards to humans (Network Operators, Reviewers).

- **MCP (Model Context Protocol)** – standard that defines how models:
  - Read **Resources**, call **Tools**, and use **Prompts**.
  - Connect to social platforms, databases, and commerce SDKs.

- **FastRender Pattern** – hierarchical swarm architecture:
  - Planner / Worker / Judge roles.
  - High parallelism and error recovery.

- **Agentic Commerce** – capability of agents to:
  - Autonomously execute financial transactions.
  - Manage assets and costs via on-chain protocols and Resource Governor.

- **HITL (Human-in-the-Loop)** – governance process where:
  - Humans review low-confidence or sensitive content before publication.

---

## 5. Constraints and Non-Functional Requirements

### 5.1 Regulatory and Ethical Constraints (SRS §2.4)

- **EU AI Act & transparency laws**:
  - Agents must disclose they are artificial when appropriate.
  - Logs must support auditability of decisions and actions.

- **Safety and Brand Protection**:
  - Content must be aligned with brand and persona rules.
  - Harmful or disallowed content must be systematically blocked or escalated.

### 5.2 Cost and Resource Constraints (SRS §2.4)

- High-quality LLMs and media generation are expensive.
- System must implement a **Resource Governor** that:
  - Enforces per-agent and per-campaign budgets.
  - Selects cost tiers for tasks (e.g., “daily” vs “hero” content).

### 5.3 Platform Volatility (SRS §2.4, §3.2)

- Social APIs are unstable; contracts may change or be revoked.
- MCP servers must **encapsulate platform-specific details**, allowing:
  - Zero changes to core agent logic when APIs change.
  - Safe fallback and degraded modes.

---

## 6. Constitutional / Non-Negotiable Rules

These apply to all future specifications, agents, and code.

1. **MCP-Only External IO**
   - **Rule**: Agents MUST NOT call external APIs, databases, or social platforms directly.
   - **Enforcement**: All external interactions MUST be encapsulated as MCP Resources or Tools.

2. **Hierarchical Swarm Only**
   - **Rule**: All core agent cognition MUST follow the FastRender roles (Planner, Worker, Judge).
   - **Enforcement**: No long-lived “god agents” performing end-to-end flows without Planner/Worker/Judge separation.

3. **HITL for Risky or Low-Confidence Content**
   - **Rule**: Any content with confidence below configured thresholds OR marked as sensitive (politics, health, finance, minors, etc.) MUST be escalated to HITL.
   - **Enforcement**: Judges MUST route such content to a Review Queue; Workers MUST NOT bypass this.

4. **SOUL.md as Persona Source of Truth**
   - **Rule**: Agent personas MUST be defined via version-controlled `SOUL.md` files (FR 1.0).
   - **Enforcement**: No hard-coded personas inside code; context assembly MUST read from `SOUL.md`.

5. **Traceability and Auditability**
   - **Rule**: Every action (post, transaction, deletion, escalation) MUST be traceable to:
     - Agent ID, Task ID, Planner decision, Worker execution, Judge decision, and optional HITL decision.
   - **Enforcement**: Minimum logging schema and correlation IDs across services.

6. **Multi-Tenancy Isolation**
   - **Rule**: One tenant’s agents MUST NOT access another tenant’s memories, wallets, or configuration.
   - **Enforcement**: Tenant IDs are required on all data schemas and MCP operations.

7. **Spec-First Implementation**
   - **Rule**: No production implementation MAY proceed unless:
     - Relevant functional and technical specs exist and are linked.
   - **Enforcement**: CI checks spec references; reviewers must check spec alignment.

---

## 7. Scope Boundaries

- **In scope**:
  - Single-Orchestrator model.
  - Social content lifecycle (trend → content → publish → feedback).
  - On-chain transactions for economic agency.
  - Multi-tenant SaaS control plane.

- **Out of scope (for this phase)**:
  - Full billing and invoicing platform.
  - Long-tail niche integrations beyond what MCP can generalize.
  - Non-digital physical world actions (e.g., physical robots).

This `_meta` file governs all subordinate specs (`functional.md`, `technical.md`, `openclaw_integration.md`) and must be updated if any high-level decision changes.

