# Project Chimera – Tooling & Skills Strategy (Task 2.3)

This document defines:

- **Developer MCP tooling** to help _me_ build and debug Chimera inside Cursor.
- **Runtime skills scaffolding** that Chimera agents (Planner / Worker / Judge) will call at run time.

Chimera follows the **FastRender Swarm** pattern (Planner, Worker, Judge) and the **Model Context Protocol (MCP)** for all external I/O, per SRS §3.1–3.2. All tools and skills below must respect that architecture and the non‑negotiable rules in `specs/_meta.md`.

---

## A. Developer MCP Tools (for building Chimera)

These MCP servers are for **developer productivity inside Cursor**, not for the runtime Chimera agents. They help with version control, file operations, research, and time‑stamped logging.

### A.1 `git-mcp` – Version Control & Diffs

- **Purpose**
  - Interact with the Git repository from the agent:
    - Inspect status, diffs, branches.
    - Stage or revert changes in a controlled way.
  - Maintain spec/code alignment by making it easy to see what changed after edits.
- **Why**
  - Supports the SRS emphasis on **traceability** and the challenge requirement to keep a clean commit story.
  - Helpful when verifying that implementations still match contracts in `specs/technical.md`.
- **How to Run (local stdio)**
  - Install via `uvx` or pipx:
    - `uvx mcp-server-git` (if packaged) or
    - Clone from `github.com/modelcontextprotocol/servers` (or equivalent) and run:
      - `python -m mcp_server_git` (stdio mode).
  - Configure in `.cursor/mcp.json` as a local stdio server (example):
    - `"command": "uvx", "args": ["mcp-server-git"]`
- **Security**
  - Scope the working directory to the Chimera repo root.
  - Do not allow operations that rewrite history (no `git push --force`) from the agent.

### A.2 `filesystem-mcp` – File Read/Edit Within Repo

- **Purpose**
  - Provide structured, auditable file access:
    - Read and write markdown specs.
    - Edit Python modules and tests.
  - Keep all edits **inside** the repository and under Git control.
- **Why**
  - Aligns with Spec‑Driven Development:
    - Agent can read `specs/*.md` and `research/*.md` before proposing code.
    - Keeps changes small and traceable.
- **How to Run**
  - Use a filesystem MCP server (e.g., `mcp-server-fs`) with:
    - `root` set to this project directory.
    - stdio transport.
  - Example command:
    - `uvx mcp-server-fs --root /path/to/project-chimera`
- **Security**
  - Restrict root to this project folder.
  - Disallow execution of arbitrary binaries from filesystem‑mcp; use it only for file content.

### A.3 `fetch` / `web-search` MCP – Research External Docs

- **Purpose**
  - Fetch and summarize:
    - The a16z “trillion‑dollar AI stack” article.
    - OpenClaw / MoltBook posts and docs.
    - API docs for MCP and Coinbase AgentKit.
- **Why**
  - Supports Task 1.1 research and ongoing design choices (e.g., which vector DB).
  - Allows the agent to ground new specs and changes in up‑to‑date external information.
- **How to Run**
  - Use a generic HTTP or search MCP server (e.g., `mcp-server-http`, `mcp-server-web-search`).
  - Configure as a remote (HTTP/SSE) MCP server with rate limits.
- **Security**
  - Only allow outbound HTTP(S); no credentials should be embedded in specs.
  - Avoid hitting private or internal services from this project context.

### A.4 `time-mcp` – Timestamps & Temporal Reasoning

- **Purpose**
  - Provide current timestamps and maybe simple time calculations.
  - Useful for:
    - Generating temporal test data.
    - Logging when specs/tests were last updated.
- **Why**
  - Helps the agent align test expectations with relative timelines (campaign start/end).
  - Keeps logs and telemetry consistent with Resource Governor and budget periods.
- **How to Run**
  - Simple local stdio server (e.g., `mcp-server-time`) that exposes:
    - `now` tool → returns ISO 8601 timestamp.
    - Optional helpers for durations.
- **Security**
  - No external network calls; purely local system time.

### A.5 `weaviate-mcp` (Stubbed) – Future Semantic Memory Testing

- **Purpose**
  - Provide a future bridge to a local or test Weaviate instance.
  - Let the agent experiment with memory schemas and `search_memory` / `upsert_memory` tools in a safe sandbox.
- **Why**
  - Directly tests SRS FR 1.1 / FR 1.2 and the memory model defined in `specs/technical.md`.
  - Prepares runtime integration for true long‑term memory.
- **How to Run**
  - Initially as a **stub**:
    - Mock responses that approximate real Weaviate search results.
  - Later, point to a real Weaviate URL via environment variables:
    - `WEAVIATE_URL=http://localhost:8080`.
- **Security**
  - Use a separate **test** index / class namespace for development.
  - Never point at production memory from the development MCP client in Cursor.

---

## B. Runtime Skills Strategy (for Chimera Agents)

Runtime skills are **logical capability packages** that Workers (and sometimes Planners or Judges) call as part of the FastRender Swarm. They wrap one or more MCP Tools/Resources into a cohesive flow, enforce policies, and expose a **clear JSON contract**.

In this repo, skills live under `skills/` and are documented via README files (no full implementation yet). Each skill definition includes:

- Description / purpose.
- Input and output schemas (JSON examples).
- Preconditions (e.g., which MCP servers must be available).
- Dependencies (which MCP tools they orchestrate).
- High‑level execution flow.

The initial critical skills (from SRS) are:

1. `trend_detection_alerting` – Perception FR 2.2.
2. `multimodal_content_generation` – Creative FR 3.0–3.2.
3. `autonomous_transaction` – Commerce FR 5.0–5.2.

See `skills/README.md` and each skill subfolder for detailed contracts.

---

## C. Summary

- **Developer MCP servers** (git, filesystem, fetch/web, time, weaviate stub) equip the Cursor agent to:
  - Read and maintain specs.
  - Safely edit code and tests.
  - Ground decisions in external research.
  - Prepare for semantic memory integration.
- **Runtime skills** in `skills/` define the **executable intent** for Chimera agents:
  - Perception (trend detection).
  - Creative engine (multimodal generation with character consistency).
  - Agentic commerce (budget‑aware on‑chain transactions).

All tools and skills must follow the constitutional rules in `specs/_meta.md`, the SRS, and `.cursor/rules/agent.mdc` (Prime Directive, MCP‑only IO, FastRender Swarm, HITL, and Spec‑Driven Development).

