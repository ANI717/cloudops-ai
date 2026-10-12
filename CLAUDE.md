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
- Backend layout (`backend/app/`): `api/routes/` for HTTP routers only (one module per resource, registered in `api/main.py`), `schemas/` for Pydantic models, `services/` for business logic, `core/config.py` for app-wide settings, `utils/` for small shared helpers. One module per resource with matching names.
- Backend code quality: ruff (lint + format) and mypy (strict, with the pydantic plugin), configured in `backend/pyproject.toml`.
- CI: GitHub Actions workflow (`.github/workflows/ci.yml`) runs ruff, mypy, and pytest on pushes to `main` and on pull requests. Actions are pinned to commit SHAs.

Current objective: Establish the development environment. Next proposed step: pre-commit hooks. Then: a branch + PR workflow.
