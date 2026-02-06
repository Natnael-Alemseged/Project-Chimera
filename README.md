# Project Chimera: Autonomous Influencer Network

> **An autonomous AI influencer system built with FastRender Swarm architecture and Model Context Protocol (MCP)**

Project Chimera transforms static content schedulers into **persistent, goal-directed digital agents** capable of perception, reasoning, creative expression, and economic agency. The system supports a fleet of thousands of virtual influencers managed by a single human Super-Orchestrator.

## 🏗 Architecture

### Core Patterns

- **FastRender Swarm** – Hierarchical agent architecture:
  - **Planner**: Decomposes high-level goals into task DAGs
  - **Worker**: Executes atomic tasks in parallel
  - **Judge**: Validates outputs with OCC and safety rules

- **Model Context Protocol (MCP)** – Universal interface for all external interactions:
  - **Resources**: Passive data streams (mentions, news, market data)
  - **Tools**: Executable actions (post content, generate media, send transactions)
  - **Prompts**: Reusable reasoning templates

- **Agentic Commerce** – Non-custodial wallets via Coinbase AgentKit for autonomous transactions

### Key Features

- ✅ **Spec-Driven Development** – All code aligns with `specs/` directory
- ✅ **Human-in-the-Loop (HITL)** – Safety layer for low-confidence or sensitive content
- ✅ **Multi-Tenancy** – Strict isolation between tenants
- ✅ **Budget Governance** – Resource Governor enforces per-agent and per-campaign limits
- ✅ **EU AI Act Compliance** – Transparency and auditability built-in

## 📁 Project Structure

```
.
├── specs/                    # Master specifications (source of truth)
│   ├── _meta.md              # Constitutional rules and vision
│   ├── functional.md         # User stories and functional requirements
│   ├── technical.md          # API contracts, schemas, infrastructure
│   └── openclaw_integration.md # Agent social network integration
├── skills/                    # Runtime skill contracts (no implementation yet)
│   ├── trend_detection_alerting/
│   ├── multimodal_content_generation/
│   └── autonomous_transaction/
├── tests/                     # TDD test suite (failing tests define contracts)
│   ├── test_trend_fetcher.py
│   └── test_skills_interface.py
├── research/                  # Architecture and tooling strategy
│   ├── architecture_strategy.md
│   └── tooling_strategy.md
├── scripts/                   # Automation scripts
│   └── spec-check.sh         # Verifies spec alignment
├── Dockerfile                 # Multi-stage containerization
├── Makefile                  # Development automation
├── pyproject.toml            # Python project config (uv)
└── .github/workflows/        # CI/CD pipelines
    └── main.yml
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)
- Docker (for containerized testing)

### Setup

```bash
# Clone the repository
git clone https://github.com/Natnael-Alemseged/Project-Chimera.git
cd Project-Chimera

# Install dependencies
make setup
# or manually: uv sync

# Run tests (builds Docker image and runs pytest)
make test

# Check spec alignment
make spec-check
```

## 🧪 Development Workflow

### Spec-Driven Development (SDD)

1. **Read specs first**: Always check `specs/` before writing code
2. **Update specs if needed**: If requirements change, update specs first
3. **Write failing tests**: Define contracts in `tests/` (TDD)
4. **Implement to pass tests**: Code must satisfy test contracts
5. **Verify spec alignment**: Run `make spec-check`

### Key Rules (from `specs/_meta.md`)

- ✅ **MCP-Only External IO** – Never call external APIs directly
- ✅ **FastRender Swarm Only** – Planner/Worker/Judge pattern required
- ✅ **HITL for Risky Content** – Low-confidence or sensitive content must escalate
- ✅ **SOUL.md as Persona Source** – Personas defined in version-controlled files
- ✅ **Multi-Tenancy Isolation** – Always include `tenant_id` in schemas

### Makefile Commands

```bash
make setup      # Install dependencies with uv sync
make test       # Run tests in Docker container
make build      # Build Docker image (chimera-fde:latest)
make spec-check # Verify code references specs/ and SRS terms
make demo       # Run small demo (contract validation + Judge/HITL logic)
make clean      # Remove Docker image and build artifacts
make help       # Show all available targets
```

### Small Demo

A minimal runnable demo shows contract validation and Judge decision logic (no backend or MCP required):

```bash
make demo
# or: uv run python scripts/demo_chimera.py
```

It validates a trend-alert payload against the FR 2.2 contract, rejects invalid input (e.g. score > 1.0), and simulates Judge routing: **Auto-Approve** (≥0.90), **HITL Review** (0.70–0.90), **Reject** (&lt;0.70).

## 🧪 Testing

Tests are written using **Test-Driven Development (TDD)**:

- Tests define contracts before implementation
- Currently **5 tests fail** (expected – implementations don't exist yet)
- Tests validate:
  - Input/output schemas (Pydantic models)
  - Skill contracts (trend detection, content generation, transactions)
  - Spec alignment

```bash
# Run tests locally
uv run pytest tests/ -v

# Run tests in Docker
make test
```

## 🔄 CI/CD

### GitHub Actions

Automated CI runs on every push and pull request:

- ✅ Installs dependencies with `uv`
- ✅ Runs tests in Docker container
- ✅ Verifies spec alignment

See `.github/workflows/main.yml` for details.

### CodeRabbit AI Review

PRs are automatically reviewed by CodeRabbit AI for:

- Spec alignment (`specs/_meta.md`, `functional.md`, `technical.md`)
- Architecture compliance (FastRender Swarm, MCP-only IO)
- Security (secrets, wallet keys, budget guards)
- Code quality (pydantic, typing, tests)

See `.coderabbit.yaml` for configuration.

## 📚 Documentation

- **Specifications**: `specs/` directory (source of truth)
- **Architecture**: `research/architecture_strategy.md`
- **Tooling**: `research/tooling_strategy.md`
- **Skills**: `skills/*/README.md` (contract definitions)
- **Security**: `SECURITY.md` (secrets, wallets, HITL, MCP)
- **Contributing**: `CONTRIBUTING.md` (commit conventions, spec-first workflow)
- **Backend scope**: `docs/BACKEND.md` (agent runtime, MCP, data layer, skills)
- **Frontend plan**: `docs/FRONTEND.md` (Dashboard & HITL UI scope)
- **Rubric alignment**: `RUBRIC_ALIGNMENT.md` (evidence for all grading criteria)
- **SRS**: `Project Chimera SRS Document Autonomous Influencer Network.pdf`

## 🛠 Tech Stack

- **Python 3.12+** – Primary language
- **uv** – Fast Python package manager
- **pydantic v2** – Data validation and settings
- **pytest** – Testing framework
- **Docker** – Containerization
- **GitHub Actions** – CI/CD
- **CodeRabbit** – AI PR review

### DB & Data Management

- **Hybrid storage** (see `specs/technical.md` §3):
  - **PostgreSQL** – Relational/transactional data (tenants, agents, campaigns, posts, wallets, transactions, users, reviews); ERD and table notes in specs.
  - **Weaviate** – Vector DB for semantic memory (RAG); Memory class schema defined in specs.
  - **Redis** – Episodic cache and task queues (Planner ↔ Worker ↔ Judge).
  - **Blockchain** (Base/Ethereum/Solana) – On-chain transaction ledger.
- All entities include `tenant_id` for multi-tenancy; no cross-tenant data access.

### MCP Configuration

- **Tenx MCP Sense** is configured in `.cursor/mcp.json` for telemetry and “thinking” verification (same GitHub account as repo).
- **Developer MCP tools** (git, filesystem, fetch, time, weaviate stub) are documented in `research/tooling_strategy.md` with setup and security notes.
- **Runtime MCP servers** (twitter, weaviate, coinbase, news) and their Resources/Tools are defined in `specs/technical.md` §4 and `specs/openclaw_integration.md`.
- All external IO must go through MCP (see `.cursor/rules/agent.mdc` and `specs/_meta.md`).

## 🎯 Current Status

This repository contains the **foundation and specifications** for Project Chimera:

- ✅ Architecture strategy and research
- ✅ Master specifications (`specs/`)
- ✅ Skill contracts (`skills/`)
- ✅ Failing TDD tests (`tests/`)
- ✅ Dockerization and automation (`Dockerfile`, `Makefile`)
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ AI governance (CodeRabbit)

**Next Steps**: Implement skills and core agent runtime to satisfy test contracts.

### Agentic Trajectory & Growth

This repo is designed so **AI agents can enter and build features with minimal human conflict**:

- **Spec-first:** `specs/` and `.cursor/rules/agent.mdc` give agents a single source of truth and clear constraints (FastRender, MCP-only, HITL, budget governance).
- **Traceability:** Rules require “explain your plan before writing code” and reference to specs/SRS, so agent changes stay aligned.
- **CONTRIBUTING.md** asks contributors to keep rules and specs updated for agent-assisted development.
- **Tenx MCP Sense** telemetry records agent-assisted work for evaluators; connect with the same GitHub account as the repo.

## 📖 References

- **SRS Document**: See `Project Chimera SRS Document Autonomous Influencer Network.pdf`
- **MCP Specification**: https://modelcontextprotocol.io
- **FastRender Pattern**: Referenced in SRS §3.1
- **uv Documentation**: https://github.com/astral-sh/uv

## 🤝 Contributing

This is a training project for the **10 Academy FDE Trainee Challenge**. All code must:

1. Align with `specs/` directory
2. Pass existing tests
3. Follow FastRender Swarm architecture
4. Use MCP for all external interactions
5. Include proper HITL escalation

See `.cursor/rules/agent.mdc` for detailed development rules.


---

**Built with ❤️ for autonomous AI influencer systems**
