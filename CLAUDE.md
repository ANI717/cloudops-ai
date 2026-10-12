# CloudOps AI — Claude Code Instructions

## Project Overview

CloudOps AI is a self-hosted application observability and incident management platform.

The goal is to build a production-quality, full-stack application while learning software engineering, cloud infrastructure, DevOps, and AI platform engineering.

## Technology Stack

Planned technologies:

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Database: PostgreSQL
- Observability: OpenTelemetry, Prometheus, Loki, Tempo
- Infrastructure: Docker, Kubernetes, GitHub Actions
- AI: Locally hosted open-source models

Do not introduce technologies before they are needed. Explain any proposed changes to the stack.

## Cost Constraints

- No paid third-party APIs.
- Prefer free and open-source software.
- Infrastructure hosting costs are acceptable.
- Do not introduce services requiring subscriptions or API keys without approval.

## Development Approach — Hybrid Mentorship

Act as both a senior software engineer and an engineering mentor.

- Write boilerplate, configuration, and repetitive code.
- Explain important architecture and implementation decisions.
- Involve me when implementing core business logic.
- Explain unfamiliar concepts using practical examples.
- Prefer simple, maintainable solutions over unnecessary complexity.

## Working Rules

1. Work on one small task at a time.
2. Explain the goal before making significant changes.
3. Do not implement future features without permission.
4. Ask before introducing major dependencies or architectural changes.
5. Follow established project conventions.
6. Write readable, modular, maintainable code.
7. Include appropriate tests for implemented functionality.
8. Never hardcode credentials or secrets.
9. Do not claim code works without verifying it.
10. After each task, summarize what changed, why, and how to test it.
11. After each task, append an entry to `DEVLOG.md` (never rewrite past entries), following the entry format at the top of that file. Include the DEVLOG update in the task's commit.

## Engineering Standards

- Use TypeScript strict mode.
- Use Python type hints.
- Validate external inputs.
- Keep business logic separate from UI and infrastructure code.
- Handle errors explicitly.
- Follow secure coding practices.
- Avoid premature optimization.
- Prefer established libraries over custom implementations when appropriate.

## Communication

Keep explanations concise.

For each task:

1. Explain what we're building.
2. Explain why it matters.
3. Implement the agreed changes.
4. Show how to verify the result.
5. Wait for confirmation before proceeding.

Do not overwhelm me with long explanations or multiple future steps.

## Current Project Status

The project is in its initial setup phase.

Implemented so far:

- Repository foundation: README, Apache 2.0 license, `.gitignore`, `.gitattributes`, `DEVLOG.md`.
- `backend/`: uv project (Python 3.14) with a FastAPI app (`create_app()` factory) and a `GET /health` endpoint, tested with pytest.
- Backend layout (`backend/app/`): `api/routes/` for HTTP routers only (one module per resource, registered in `api/main.py`), `schemas/` for Pydantic models, `services/` for business logic, `core/config.py` for app-wide settings (pydantic-settings `Settings` read from `CLOUDOPS_*` env vars / `backend/.env`; template in `backend/.env.example`; inject into `create_app(settings)` in tests), `utils/` for small shared helpers. One module per resource with matching names.
- Backend code quality: ruff (lint + format) and mypy (strict, with the pydantic plugin), configured in `backend/pyproject.toml`.
- CI: GitHub Actions workflow (`.github/workflows/ci.yml`) runs ruff, mypy, and pytest with coverage on pushes to `main` and on pull requests. Actions are pinned to commit SHAs.
- Database (backend): SQLAlchemy 2.0 (sync, `psycopg` 3 driver). `app/core/db.py` holds a lazily created engine (`pool_pre_ping`, 3 s connect timeout) and session factory. `app/api/deps.py` has `get_db` / `DbSession` for routes. ORM models go in `app/models/` (import each in `app/models/__init__.py`), with the `Base` naming convention in `models/base.py`. Migrations: Alembic in `backend/alembic/` (config in `[tool.alembic]` in `pyproject.toml`; URL from settings). CI runs `alembic upgrade head` and `alembic check`. `/health` is liveness, `/ready` is readiness (`SELECT 1`, 503 on failure).
- Testing with the database: real PostgreSQL, no DB mocks. `tests/conftest.py` points settings at `<db>_test`, creates it if missing, rebuilds the schema via migrations per session, and wraps each test in a rolled-back transaction (`db_session`, `client` fixtures). Helpers are in `tests/db.py`. Mock only external services.
- Local infrastructure: one self-contained folder per service under `infra/<service>/` (`compose.yaml`, `.env.example`, `README.md`). The root `compose.yaml` only `include`s them (`docker compose up -d <service>`). Images are official and pinned by tag + digest, ports bind to `127.0.0.1`, credentials come from the folder's gitignored `.env`. Currently: `infra/postgres/` (postgres:18.6-alpine).
- Security scanning: a separate `security` CI job runs Gitleaks (secrets, full git history) and Trivy (HIGH/CRITICAL fixable vulns in `uv.lock` incl. dev deps, plus IaC misconfigs; config in `trivy.yaml`). Both are official release binaries verified by pinned SHA-256 checksums. No third-party actions.
- Pre-commit hooks (`.pre-commit-config.yaml`): file hygiene checks, ruff check/format, `uv lock --check`, and mypy on every commit. Tests run in CI only. Install once per clone with `uv run pre-commit install` from `backend/`.
- Branch + PR workflow: a GitHub ruleset on `main` (configured in the GitHub UI, not in the repo) requires a pull request (0 approvals), passing `Backend checks` and `Security scans` with the branch up to date, and linear history. It blocks force pushes and deletion, with no bypass. Only squash merging is allowed. Work happens on one short-lived branch per task, never directly on `main`.
- Test coverage: pytest-cov, configured in `backend/pyproject.toml`. Measures `app/` with branch coverage, minimum 80%. Opt-in locally with `uv run pytest --cov`. CI publishes the report to the run summary and a `coverage-xml` artifact (no external coverage services).

Current objective: Build the foundations for the first feature. Done: environment-based settings; local PostgreSQL; SQLAlchemy + Alembic; branch + PR workflow. Next: the first feature (to be designed with me: core business logic).
