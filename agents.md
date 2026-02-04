# Agent Operating Guide (Source of Truth)

## 🏗 Project Context
- **Stack (actual):**
  - Python 3.14 (CLI app, stdlib-only)
  - Node/TypeScript + React (component in `src/components/`) — minimal front-end components present
  - Git + GitHub (repo: `Natnael-Alemseged/mcp-challenge`)
  - macOS (development environment)
  - **IDE**: Cursor (configured via `.cursor/` directory)
  - **Agent**: Cursor AI
- **Current Task:** Complete the Tenx MCP Setup Challenge — implement features, tests, and CI.

## 🛠 Commands & Skills (actual)
- **Run (CLI game):**
  - Play locally: `python -m cli_game`  (or `python3 -m cli_game`)
  - Deterministic demo: `python -m cli_game --seed 42 -d easy`
- **Run tests (Python):**
  - Direct (package importable): `PYTHONPATH=cli_game python3 -m unittest cli_game.tests.test_game -v`
  - Discovery: `PYTHONPATH=cli_game python3 -m unittest discover -s cli_game/cli_game/tests -p "test_*.py" -v`
- **Frontend (where applicable):**
  - Typical commands (if/when `package.json` is added): `npm install` → `npm test` → `npm run build`
  - React component tests live at `src/components/**/__tests__` (example: `Button/__tests__/Button.test.tsx`).
- **Verification / CI:**
  - Recommended GitHub Actions: run Python tests on push + PR; verify packaging and linting for TS/React.
- **Logging:** Use `log_passage_time_trigger` for every user interaction with the agent (MCP server). Use `tenxfeedbackanalytics` for telemetry registration.

## 🏛 Architecture & decisions (so far)
- **High-level:** mono-repo style for exercises — small Python package + isolated frontend components.
- **Folder structure (current):**
  - `cli_game/` — Python package and tests
    - `cli_game/cli_game/game.py` — core logic (pure, testable)
    - `cli_game/cli_game/__main__.py` — interactive CLI wrapper
    - `cli_game/cli_game/tests/` — unit tests (stdlib unittest)
  - `src/components/...` — React + TypeScript UI components (co-located tests)
  - `.github/`, `.cursor/`, `REPORT.md`, `agents.md`, `implementation_plan.md`
- **Naming conventions:**
  - Python package: `snake_case` (package name `cli_game`)
  - Python modules/classes: `snake_case` for modules, `PascalCase` for classes (`Game`)
  - CLI entry: `python -m cli_game` (module invocation)
  - JS/TS React components: `PascalCase` for components, `kebab-case` or `camelCase` for file names where appropriate (current: `Button/Button.tsx`)
  - Tests colocated with implementation (`__tests__` next to component / `tests/` in Python package)
- **API / integration notes:**
  - The MCP server (`tenxfeedbackanalytics`) is an HTTP ingest endpoint — authenticate via `Authorization: Bearer <token>` when registering repos.
  - Do NOT use MCP endpoint as a git remote — it's an API only.

## ✅ Development rules (enforced)
- Create `implementation_plan.md` before non-trivial changes.
- Add unit tests for new logic and ensure they run locally before pushing.
- Commit messages: conventional-ish (feat/, fix/, chore/, docs/). Keep them concise.
- Add minimal CI to run tests on push/PR (GH Actions recommended).

### UI Standards (enforced for all future UI components) 🔧
- **All `button` components must include a subtle scale-on-hover interaction:** `transition transform hover:scale-105` (or equivalent CSS). This rule is mandatory for every new or updated UI component unless a documented exception is approved.
- **Implementation guidance:**
  - Tailwind: `class="transition transform hover:scale-105"` on the root `button` element.
  - CSS fallback (vanilla): `transition: transform .12s ease-in-out;` and `button:hover { transform: scale(1.05); }`.
  - Prefer implementing the effect at the **component** level (e.g., `Button.tsx`) so all usages inherit it.
- **Testing & verification:**
  - Unit: snapshot tests that assert the `className`/style on the `button` component.
  - Visual: add a Storybook story and include a Percy/Chromatic visual check for the hover state where possible.
  - PR checklist: include `UI Standards` item — `Button: hover scale applied` (auto-check via lint/test if available).
- **Enforcement:** add a linting rule or unit test in the component template; document the pattern in `src/components/Button/README.md`.

## 🔁 Verification (what I ran for this task)
- Created & pushed repo: `Natnael-Alemseged/mcp-challenge` (branch `main`).
- Implemented a small Python CLI (`cli_game`) with unit tests and verified tests locally (with `PYTHONPATH` adjustment).
- Attempted MCP registration — received HTTP 401 (requires API token).

## ⚠️ Notes / Next steps
- Add a GitHub Actions workflow to run `python -m unittest` on push. I can scaffold this for you.
- Store MCP tokens in GitHub Secrets or local secret manager — do not commit tokens to the repo.

## ⚠️ Lessons Learned
- Keep runtime & test commands explicitly documented in `agents.md` to avoid local-import issues (PYTHONPATH).
- Co-locating tests with implementation keeps changes discoverable and simplifies maintenance.
- External sources and their influence on rules are documented in [EXTERNAL_SOURCES.md](../EXTERNAL_SOURCES.md).