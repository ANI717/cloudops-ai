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
├── .pre-commit-config.yaml  # Git hooks run on every commit
├── .gitleaks.toml   # Gitleaks secret scan settings
├── trivy.yaml       # Trivy security scan settings
├── backend/         # Python backend service (managed with uv)
│   ├── app/
│   │   ├── main.py      # FastAPI app factory (create_app)
│   │   ├── api/
│   │   │   ├── main.py  # Combines all routers into api_router
│   │   │   └── routes/  # HTTP routers only
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
including dev tools (pytest, ruff, mypy, pre-commit). Re-run it after pulling changes.

Then install the git hooks (once per clone):

```bash
uv run pre-commit install
```

From then on, every `git commit` runs basic file checks, ruff (lint + format),
a `uv.lock` consistency check, and mypy on the staged files (configured in
[`.pre-commit-config.yaml`](.pre-commit-config.yaml)). If a hook fails or fixes a
file, the commit is stopped: review the changes, `git add` them, and commit again.
Run all hooks on every file with `uv run pre-commit run --all-files`.

Optionally, create a local config file (gitignored) from the template:

```bash
cp .env.example .env
```

Settings are read from environment variables prefixed with `CLOUDOPS_`, then from
`backend/.env`, then from defaults in `app/core/config.py`. Invalid values stop
the app at startup with a clear error.

| Variable               | Default       | Description                                                       |
| ---------------------- | ------------- | ----------------------------------------------------------------- |
| `CLOUDOPS_ENVIRONMENT` | `development` | `development`, `test`, or `production` (production disables `/docs`) |
| `CLOUDOPS_APP_NAME`    | `CloudOps AI` | Display name in the API docs                                      |

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

Run the tests with coverage (lists uncovered lines and fails below 80%):

```bash
uv run pytest --cov
```

Coverage is configured under `[tool.coverage.*]` in `backend/pyproject.toml`. Add
`--cov-report=html` to browse line-by-line results in `htmlcov/index.html`.

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
uv sync --locked && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest --cov
```

### Security scanning

CI runs two free, open-source scanners in a separate **Security scans** job:

- [Gitleaks](https://github.com/gitleaks/gitleaks) checks the full git history for
  accidentally committed secrets (API keys, tokens, passwords).
- [Trivy](https://trivy.dev/) checks dependencies (`backend/uv.lock`, including dev
  tools) for known HIGH/CRITICAL vulnerabilities that have a fix available, and
  infrastructure files (Dockerfiles, Kubernetes manifests) for misconfigurations.
  Settings live in [`trivy.yaml`](trivy.yaml).

To run them locally, install the tools once:

```bash
# Windows
winget install Gitleaks.Gitleaks AquaSecurity.Trivy
# macOS
brew install gitleaks trivy
```

Then, from the repository root:

```bash
gitleaks git . --redact     # scan all commits for secrets
gitleaks dir . --redact     # also scan uncommitted files (skips .venv, see .gitleaks.toml)
trivy fs .                  # scan dependencies and config files (reads trivy.yaml)
```

Each command exits non-zero if it finds a problem. The first Trivy run downloads
its vulnerability database (about 1 minute).

## License

Copyright 2026 Animesh Bala Ani

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution details.
