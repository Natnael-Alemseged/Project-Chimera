# Contributing to Project Chimera

## Spec-First and Rule Compliance

- **Read `specs/` before writing code.** The Prime Directive in `.cursor/rules/agent.mdc` is: never generate code without checking specs first.
- **Explain your plan before writing code** (traceability). Reference `specs/functional.md`, `specs/technical.md`, or `specs/_meta.md` as needed.
- **Keep changes small and reviewable.** Prefer multiple focused commits over one large change.

## Commit Conventions (Git Hygiene)

- **Format:** Use conventional-style prefixes:
  - `feat:` new feature or capability
  - `fix:` bug fix
  - `docs:` documentation only
  - `chore:` tooling, config, or maintenance
  - `test:` add or update tests
- **Message:** One short line (≤72 chars) summarizing the change. Example: `feat: add OpenClaw status resource to specs`.
- **Frequency:** Commit often (e.g., after each logical step) so history tells a clear story of evolving complexity.
- **No secrets:** Never commit `.env` or any file containing API keys, tokens, or private keys.

## Development Workflow

1. Create or update specs if behavior or contracts change.
2. Write or update tests (TDD: failing tests define contracts).
3. Implement to satisfy tests and specs.
4. Run `make spec-check` and `make test` (or `uv run pytest tests/ -v`).
5. Commit with a clear, conventional message.

## Branching and PRs

- Prefer working on a branch and opening a PR for non-trivial changes.
- Ensure CI passes (GitHub Actions) and that CodeRabbit and spec-check report no violations.
- Link PR description to relevant spec sections where applicable.

## Agent-Assisted Development

- The repository is designed for **agentic trajectory**: AI agents (e.g., Cursor) use `.cursor/rules/agent.mdc` and `specs/` to stay aligned. Keep rules and specs updated so agents can contribute safely and consistently.
