# CloudOps AI

A self-hosted application observability and incident management platform.

CloudOps AI collects telemetry (metrics, logs, and traces) from your applications,
presents it in a unified dashboard, and helps teams detect, investigate, and resolve
incidents, with AI assistance from locally hosted open-source models. No paid
third-party APIs required.

## Project Status

🚧 **Early setup.** The backend skeleton is in place: a FastAPI app with a
`GET /health` endpoint, tests, linting/type checking, and CI. No product features
or frontend have been built yet.

## Planned Features

- **Telemetry ingestion:** metrics, logs, and traces via OpenTelemetry
- **Dashboards:** visualize service health and performance
- **Incident management:** create, track, and resolve incidents
- **AI assistance:** local open-source models to help summarize and investigate incidents

## Tech Stack (Planned)

| Area           | Technologies                                |
| -------------- | ------------------------------------------- |
| Frontend       | Next.js, TypeScript, Tailwind CSS           |
| Backend        | Python, FastAPI                             |
| Database       | PostgreSQL                                  |
| Observability  | OpenTelemetry, Prometheus, Loki, Tempo      |
| Infrastructure | Docker, Kubernetes, GitHub Actions          |
| AI             | Locally hosted open-source models           |

Technologies are introduced incrementally, only when they are needed.

## Repository Structure

```text
cloudops-ai/
├── .github/
│   └── workflows/
│       └── ci.yml   # CI: lint, format check, type check, tests
├── backend/         # Python backend service (managed with uv)
│   ├── app/
│   │   ├── main.py      # FastAPI app factory (create_app)
│   │   ├── api/routes/  # HTTP routers only
│   │   ├── core/        # App-wide settings (config.py)
│   │   ├── schemas/     # Pydantic request/response models
│   │   ├── services/    # Business logic
│   │   └── utils/       # Small shared helpers
│   ├── tests/           # pytest tests
│   ├── pyproject.toml   # Dependencies and tool config
│   └── uv.lock          # Exact locked dependency versions
├── CLAUDE.md        # Instructions for AI-assisted development
├── DEVLOG.md        # Running log of changes, one entry per task
├── LICENSE          # Apache License 2.0
├── NOTICE           # Copyright notice
└── README.md
```

A `frontend/` directory will be added as development progresses.

## Prerequisites

- [Git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/): Python package and environment manager

Install uv (you don't need to install Python separately; uv handles it):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Needed later:

- [Node.js](https://nodejs.org/) (LTS) for the frontend
- [Docker](https://docs.docker.com/get-docker/) for local services

## Getting Started

```bash
git clone https://github.com/ANI717/cloudops-ai.git
cd cloudops-ai
```

### Backend

All backend commands run from the `backend/` directory.

**1. Set up the environment**

```bash
cd backend
uv sync
```

`uv sync` installs the pinned Python version (3.14) if needed, creates a virtual
environment in `backend/.venv`, and installs the exact dependencies from `uv.lock`,
including dev tools (pytest, ruff, mypy). Re-run it after pulling changes.

**2. Run the development server**

```bash
uv run fastapi dev app/main.py
```

The server auto-reloads on code changes. Stop it with `Ctrl+C`.

- Health check: <http://127.0.0.1:8000/health>
- Interactive API docs: <http://127.0.0.1:8000/docs>

```bash
curl http://127.0.0.1:8000/health   # {"status":"ok"}
```

**3. Run the tests**

```bash
uv run pytest       # add -v for one line per test
```

**4. Lint, format, and type-check** (configured in `backend/pyproject.toml`)

```bash
uv run ruff check .          # lint (add --fix to auto-fix safe issues)
uv run ruff format .         # format code (use --check to verify only)
uv run mypy                  # strict static type checking
```

**5. Run all CI checks locally**

The same checks [CI](.github/workflows/ci.yml) runs on every push to `main` and
every pull request:

```bash
uv sync --locked && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```

## License

Copyright 2026 Animesh Bala Ani

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution details.
