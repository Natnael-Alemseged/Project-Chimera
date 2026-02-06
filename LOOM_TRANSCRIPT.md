# Project Chimera - Loom Video Transcript (5 Minutes)

## Script Overview
**Duration**: ~5 minutes  
**Purpose**: Demonstrate spec structure, TDD approach, IDE agent context, and MCP telemetry

---

## [0:00-0:30] Introduction & Repository Overview

**Script:**
"Hi, I'm [Your Name], and this is my submission for the Project Chimera FDE Trainee Challenge. Let me walk you through what I've built.

First, let's look at the repository structure. As you can see, we have:
- `specs/` directory with our master specifications
- `tests/` with failing TDD tests
- `skills/` with runtime skill contracts
- `Dockerfile` and `Makefile` for automation
- `.github/workflows/` for CI/CD
- And `.cursor/rules/` for IDE agent governance

This follows the Spec-Driven Development approach required by the challenge."

**Visual Actions:**
- Show repository root
- Navigate through key directories
- Highlight file structure

---

## [0:30-2:00] Spec Structure & OpenClaw Integration Plan

**Script:**
"Let me show you the spec structure. We have four key specification files:

First, `specs/_meta.md` - this is our constitution. It defines non-negotiable rules like 'MCP-only external IO' and 'FastRender Swarm only'. This ensures all code follows the architectural patterns.

Next, `specs/functional.md` - user stories in 'As a [role], I need [capability]' format. These cover Planner, Worker, Judge, and HITL Reviewer personas.

`specs/technical.md` contains executable specs - JSON schemas for API contracts, Mermaid ERDs for database design, and MCP tool definitions. Notice the Task payload schema here - this is what Workers consume.

Finally, `specs/openclaw_integration.md` - our agent social network plan. This defines how Chimera agents publish availability via MCP Resources like `agent://status/availability`, and how they share trend signals and collaborate with other agents. The Mermaid diagram shows the integration topology through the MCP bridge layer.

All specs are linked and traceable - every code change can reference back to these."

**Visual Actions:**
- Open `specs/_meta.md`, scroll through constitutional rules
- Open `specs/functional.md`, show user stories
- Open `specs/technical.md`, highlight JSON schemas and ERD
- Open `specs/openclaw_integration.md`, show MCP Resource/Tool definitions and diagram

---

## [2:00-3:30] Failing Tests Running (TDD Approach)

**Script:**
"Now let's demonstrate the TDD approach. I'll run the test suite.

[Run: `uv run pytest tests/ -v`]

As you can see, we have 7 tests total:
- 5 tests are **failing** - this is intentional and expected
- 2 tests are passing - one validates Pydantic models, one is a placeholder

The failures are because the implementations don't exist yet. This is true TDD - we wrote the tests first to define the contracts. For example, `test_trend_detection_alerting_contract` fails because `execute_trend_detection` doesn't exist yet. The test defines exactly what the function signature and output should look like.

Similarly, `test_skills_interface.py` validates the input/output contracts for all three skills - trend detection, multimodal content generation, and autonomous transactions. These tests use Pydantic models to enforce strict schemas.

This proves we're following TDD - the tests define the 'empty slots' that future implementations must fill."

**Visual Actions:**
- Run pytest command in terminal
- Show test output (5 failed, 2 passed)
- Open `tests/test_skills_interface.py`, show Pydantic models
- Explain that failures are expected and define contracts

---

## [3:30-4:30] IDE Agent Context Demonstration

**Script:**
"Now let's demonstrate that our IDE agent understands the project context. I'll ask it a question about the architecture.

[Type in Cursor chat: 'How does the Judge agent validate content before publishing?']

Perfect! The agent references `specs/_meta.md` and `specs/functional.md`, explains the HITL escalation process, and mentions confidence thresholds. Notice it's using our rules from `.cursor/rules/agent.mdc` - it's checking specs first, explaining the plan, and referencing SRS sections.

Let me ask another question about MCP.

[Type: 'Can I call the Twitter API directly from a Worker?']

Excellent! The agent correctly says 'No' and references the constitutional rule about MCP-only external IO. It suggests using an MCP server instead. This proves our agent rules are working - it's enforcing the architecture constraints we defined.

The agent is acting as a co-pilot that understands Project Chimera's specific patterns and constraints."

**Visual Actions:**
- Open Cursor chat/agent panel
- Type questions about Judge validation and MCP usage
- Show agent responses referencing specs and rules
- Highlight that agent enforces architectural constraints

---

## [4:30-5:00] MCP Telemetry & Conclusion

**Script:**
"Finally, I want to confirm that Tenx MCP Sense has been active throughout this entire development process. As you can see in the MCP panel, the connection is active and logging telemetry.

All my interactions with the IDE agent have been logged, including:
- Architecture decisions
- Spec creation
- Test writing
- Code reviews

The telemetry shows my 'thinking' process - how I approached each task, what questions I asked, and how the agent guided me. This is connected to my GitHub account [Your GitHub Username], which matches the repository.

In summary, I've delivered:
- ✅ Executable specs with API schemas and ERDs
- ✅ Strategic tooling separation (Dev MCPs vs Runtime Skills)
- ✅ True TDD with failing tests defining contracts
- ✅ Governance pipeline with CI/CD, linting, and security checks
- ✅ OpenClaw integration plan with MCP protocols

This repository is ready for AI agents to enter and build the final features with minimal human conflict. Thank you!"

**Visual Actions:**
- Show MCP Sense connection status
- Show telemetry/logs (if visible)
- Confirm GitHub account connection
- Summarize deliverables
- End screen with repository URL

---

## Key Points to Emphasize

1. **Spec Fidelity**: Executable specs (JSON schemas, ERDs, MCP protocols) - not just text
2. **Tooling Strategy**: Clear separation documented in `research/tooling_strategy.md`
3. **TDD**: Failing tests prove we wrote tests first
4. **CI/CD**: GitHub Actions + CodeRabbit governance pipeline
5. **OpenClaw**: Detailed integration plan with MCP Resources/Tools
6. **Agent Context**: IDE agent enforces rules and references specs

---

## Technical Notes for Recording

- **Screen Resolution**: 1920x1080 recommended
- **Zoom Level**: 100-125% for code readability
- **Terminal Font**: Use monospace, size 12-14
- **Cursor Speed**: Move cursor deliberately, pause on important sections
- **Audio**: Clear narration, minimal background noise
- **Timing**: Keep each section within allocated time slots

---

## Post-Recording Checklist

- [ ] Upload to Loom
- [ ] Set video to public/unlisted
- [ ] Copy shareable link
- [ ] Add link to submission form
- [ ] Verify MCP Sense telemetry is accessible to evaluators
