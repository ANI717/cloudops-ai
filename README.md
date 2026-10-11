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
├── CLAUDE.md        # Instructions for AI-assisted development
├── LICENSE          # Apache License 2.0
├── NOTICE           # Copyright notice
└── README.md
```

`backend/` and `frontend/` directories will be added as development progresses.

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

Setup and run instructions will be added as components are implemented.

## License

Copyright 2026 Animesh Bala Ani

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution details.
