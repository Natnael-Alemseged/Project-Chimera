# Security

## Overview

Project Chimera handles multi-tenant agent data, financial operations (Agentic Commerce), and external integrations. Security is enforced via specs, rules, and tooling.

## Secrets Management

- **Never commit secrets.** `.gitignore` excludes `.env` and env-specific files.
- **Use `.env.example`** for required variable names only (no values).
- **Runtime secrets** (API keys, MCP tokens, Coinbase credentials) must be supplied via environment or a secrets manager; never hardcoded.
- **CI/CD**: Use GitHub Secrets for any tokens needed in workflows; no secrets in repository or logs.

## Wallet & Financial Security

- **Non-custodial wallets only** (Coinbase AgentKit). Private keys never live in application code or config.
- **Budget guards** are mandatory: every transaction flow must validate against `budget_guard` (max_per_tx, max_daily, max_campaign_total) per `specs/technical.md` and `skills/autonomous_transaction/README.md`.
- **CFO Judge / Resource Governor** must approve or deny financial operations; no bypass.

## API & External Access

- **MCP-only external IO.** Workers must not call Twitter, Weaviate, Coinbase, or any external API directly. All external access goes through MCP Resources and Tools (see `specs/_meta.md`).
- **Tenant isolation:** All data access and MCP operations must be scoped by `tenant_id`; no cross-tenant data leakage.

## Content & Safety

- **HITL (Human-in-the-Loop)** is required for low-confidence content (< 0.90) and sensitive topics (politics, finance, health, minors). Judges must escalate; no auto-publish of high-risk content (see `specs/functional.md`, `.cursor/rules/agent.mdc`).
- **OCC (Optimistic Concurrency Control):** Judges must validate `state_snapshot_version` before committing; no blind commits that ignore campaign state changes.

## Governance & Scanning

- **CodeRabbit** is configured (`.coderabbit.yaml`) to flag: secrets exposure, improper wallet key handling, missing OCC, budget overrun risks, and direct API calls.
- **gitleaks** is enabled in CodeRabbit for secrets scanning.
- **`make spec-check`** verifies code references specs and SRS terms; run before pushing.

## Reporting

If you find a security issue, do not open a public issue. Report via the project maintainers or 10 Academy channel as appropriate.
