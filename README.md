# CloudOps AI

A self-hosted application observability and incident management platform.

CloudOps AI collects telemetry (metrics, logs, and traces) from your applications,
presents it in a unified dashboard, and helps teams detect, investigate, and resolve
incidents, with AI assistance from locally hosted open-source models. No paid
third-party APIs required.

## Project Status

🚧 **Early setup.** No application code has been implemented yet. The project
structure and development environment are being established.

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
├── backend/         # Python backend service (managed with uv)
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

Needed later:

- [Node.js](https://nodejs.org/) (LTS) for the frontend
- [Docker](https://docs.docker.com/get-docker/) for local services

## Getting Started

```bash
git clone https://github.com/ANI717/cloudops-ai.git
cd cloudops-ai
```

### Backend

uv installs the pinned Python version (if needed), creates a virtual environment
in `backend/.venv`, and installs the exact dependencies from `uv.lock`:

```bash
cd backend
uv sync
uv run python --version   # Python 3.14.x
```

Run the development server (auto-reloads on code changes):

```bash
uv run fastapi dev app/main.py
```

- Health check: <http://127.0.0.1:8000/health>
- Interactive API docs: <http://127.0.0.1:8000/docs>

Run the tests:

```bash
uv run pytest
```

## License

Copyright 2026 Animesh Bala Ani

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution details.
