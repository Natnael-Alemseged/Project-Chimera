# Project Chimera – Functional Specification

This document captures **user stories** for key actors in Project Chimera, grouped by functional area. Stories follow the format:

> As a **[role]**, I need **[capability]** so that **[benefit]**.

---

## 1. Cognitive Core & Persona Management (SRS §4.1)

### 1.1 SOUL.md Personas (FR 1.0, FR 1.2)

- As a **Developer**, I need to define each agent’s persona in a `SOUL.md` file so that I can version-control backstory, voice, values, and directives.
- As a **Chimera Agent**, I need my active persona to be loaded from `SOUL.md` and long-term memories so that my responses remain consistent with my identity over time.
- As a **Network Operator**, I need to update persona constraints (e.g., “never discuss politics”) via a single configuration file so that policy changes propagate to all relevant agents without code changes.

### 1.2 Hierarchical Memory Retrieval (FR 1.1)

- As a **Chimera Agent**, I need to retrieve recent episodic context from Redis so that I can respond coherently to ongoing conversations.
- As a **Chimera Agent**, I need to fetch semantically relevant memories from Weaviate so that I can recall long-term history (e.g., prior campaigns, past collaborations).
- As a **Judge**, I need access to the same assembled context the Worker used so that I can fairly evaluate whether the output is on-brand and safe.

---

## 2. Perception System (Data Ingestion) (SRS §4.2)

### 2.1 Active Resource Monitoring (FR 2.0)

- As a **Chimera Agent**, I need to poll MCP Resources for:
  - social mentions,
  - niche news (e.g., `news://ethiopia/fashion/trends`),
  - market prices,
  so that I can react in near-real-time to context changes.

- As a **Planner**, I need to subscribe to relevant Resource updates so that I can create or adjust tasks when meaningful events occur.

### 2.2 Semantic Filtering & Relevance Scoring (FR 2.1)

- As a **Planner**, I need incoming Resource items to be scored for relevance using a cheap LLM so that only high-signal events create tasks, controlling cost and noise.
- As a **Network Operator**, I need to configure relevance thresholds per campaign so that I can tune sensitivity for different brands and goals.

### 2.3 Trend Detection (FR 2.2)

- As a **Trend Spotter Worker**, I need to analyze aggregated news and social data over time windows so that I can emit “Trend Alerts” for emerging topics.
- As a **Planner**, I need to receive “Trend Alerts” as structured events so that I can prioritize content pipeline tasks around them.

---

## 3. Creative Engine (Content Generation) (SRS §4.3)

### 3.1 Multimodal Generation via MCP Tools (FR 3.0)

- As a **Worker**, I need to generate text captions using high-quality LLMs so that I can produce engaging posts aligned with the agent persona.
- As a **Worker**, I need to generate images via MCP tools (e.g., `mcp-server-ideogram`) so that the agent can produce visual content.
- As a **Worker**, I need to call video generation tools (e.g., `mcp-server-runway`) so that I can produce hero video content for key campaigns.

### 3.2 Character Consistency Lock (FR 3.1)

- As a **Worker**, I need to automatically include a `character_reference_id` or style identifier when requesting images so that the influencer remains visually consistent across posts.
- As a **Judge**, I need to verify that generated images match the canonical agent appearance so that off-model or inconsistent visuals are rejected.

### 3.3 Tiered Video Rendering (FR 3.2)

- As a **Planner**, I need to decide between “daily” lightweight video content and “hero” high-fidelity content so that we balance engagement and cost.
- As a **Resource Governor**, I need visibility into per-campaign and per-agent media spend so that I can prevent budget overruns.

---

## 4. Action System (Publishing and Engagement) (SRS §4.4+)

### 4.1 Content Scheduling and Publishing

- As a **Planner**, I need to schedule posts with timing, platform, and targeting metadata so that Workers can publish at optimal times.
- As a **Worker**, I need to call MCP Tools like `post_content` with structured payloads so that publishing is reliable and auditable.
- As a **Network Operator**, I need a dashboard to view scheduled and recently published content so that I can supervise and intervene when needed.

### 4.2 Replies and Engagement

- As a **Chimera Agent**, I need to process incoming comments/mentions via Resources so that I can decide whether to reply, ignore, or escalate.
- As a **Worker**, I need to draft replies that follow persona and safety constraints so that engagement remains on-brand and low-risk.
- As a **Judge**, I need to apply moderation rules and HITL routing to replies so that controversial interactions are properly handled.

---

## 5. Agentic Commerce (SRS §1.3, §4.6)

### 5.1 Wallet Management

- As a **Chimera Agent**, I need a non-custodial crypto wallet (Coinbase AgentKit) so that I can autonomously receive payments and pay for services.
- As a **Resource Governor**, I need to set per-agent and per-campaign spend limits so that agents cannot overspend on ads or generation APIs.
- As a **Network Operator**, I need visibility into an agent’s P&L so that I can measure ROI and adjust strategy.

### 5.2 On-Chain Transactions

- As a **Worker**, I need to call an MCP Tool like `send_transaction` with structured parameters so that I can safely execute on-chain payments.
- As a **Judge**, I need to validate that any financial operation is within risk thresholds and policy so that unauthorized or suspicious transactions are blocked or escalated.
- As a **Compliance Officer**, I need an audit trail of all on-chain actions so that I can prove regulatory compliance.

---

## 6. Orchestration and Governance (SRS §1.2, §3.0)

### 6.1 Task Orchestration

- As a **Planner**, I need to decompose campaign goals into a DAG of tasks so that Workers can execute them in parallel without conflicts.
- As a **Worker**, I need tasks that include clear acceptance criteria and required context so that I can execute them deterministically.
- As a **Judge**, I need to know the original task goal to evaluate whether the produced artifact meets the acceptance criteria.

### 6.2 Human-in-the-Loop (HITL) Review

- As a **Judge**, I need to compute a confidence score and risk category for each artifact so that I can decide whether to auto-approve, escalate to HITL, or reject.
- As a **HITL Reviewer**, I need a review interface with:
  - Preview of the content,
  - Confidence and risk explanation,
  - Quick actions (Approve, Edit, Reject),
  so that I can review efficiently without deep technical knowledge.

- As a **Policy Owner**, I need to define rules that always route certain topics (e.g., politics, medical advice) through HITL regardless of confidence so that we never auto-publish high-risk content.

### 6.3 Multi-Tenancy and Isolation

- As a **Platform Operator**, I need tenant-level isolation of agents, memories, and wallets so that one brand’s data is never exposed to another.
- As a **Developer**, I need tenant IDs in all key APIs and schema definitions so that I cannot accidentally mix data across tenants.

---

## 7. Developer Experience and Extensibility

### 7.1 MCP Server Extensions

- As a **Developer**, I need a way to add new MCP servers (e.g., a new social platform or internal CMS) so that agents can gain new capabilities without code changes in the core system.
- As a **Developer**, I need documentation and type-safe SDKs for defining Resources and Tools so that I can avoid inconsistent interfaces.

### 7.2 Testing and Spec Alignment

- As a **Developer**, I need to write failing tests (e.g., `test_trend_fetcher.py`, `test_skills_interface.py`) based on `specs/technical.md` so that agents (or humans) can later implement functionality to satisfy those tests.
- As a **Reviewer (human or AI)**, I need clear references from PRs to specific spec sections so that I can verify spec alignment before approving changes.

