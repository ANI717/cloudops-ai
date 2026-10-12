# Development Log

A running log of changes made to CloudOps AI, one entry per task, oldest first.
New entries are appended to the end.

Entry format:

```markdown
## YYYY-MM-DD — Short task title

**What changed:** files and components added, modified, or removed.
**Why:** the reason for the change and key decisions.
**How to verify:** commands or steps to confirm it works.
```

Each entry is committed together with the task's changes, so `git log -- DEVLOG.md`
links entries to commits. Entries written before this log existed list their commit.

---

## 2026-10-11 — Repository foundation

**What changed:**
- Rewrote `README.md` with project overview, planned features, tech stack, and prerequisites.
- Committed `CLAUDE.md` (AI-assisted development instructions).
- Added Python, uv, tooling-cache, and editor/OS entries to `.gitignore`.
- Added `.gitattributes` to normalize line endings to LF (CRLF for `.ps1`/`.bat`/`.cmd`).

**Why:**
- The original `.gitignore` was the Node template, which has no Python rules.
- Normalizing line endings to LF stops CRLF from breaking shell scripts and Dockerfiles in Linux containers and CI.
- `uv.lock` is intentionally **not** ignored, so installs are reproducible.

**How to verify:**
- `git check-ignore -v .venv/x __pycache__/x` shows both paths are ignored.
- `git check-ignore uv.lock` prints nothing, so the lock file is not ignored.
- `git ls-files --eol` shows `i/lf` for all files.

**Commit:** `de7f40a`

## 2026-10-11 — Relicense to Apache License 2.0

**What changed:**
- Replaced the MIT `LICENSE` with the official Apache 2.0 text.
- Added a `NOTICE` file with the copyright line.
- Updated the README's license section.

**Why:**
- The project switched to Apache 2.0.
- `LICENSE` is kept verbatim so tools recognize it.
- Copyright attribution lives in `NOTICE`, per the Apache convention. Section 4(d) of the license requires redistributors to keep it.

**How to verify:**
- `sha256sum LICENSE` should print `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
- `grep -rnw MIT --exclude-dir=.git .` finds nothing.

**Commit:** `5b42c28`

## 2026-10-11 — Backend project with uv and FastAPI health check

**What changed:**
- Created `backend/` as a uv project pinned to Python 3.14 (`pyproject.toml`, `.python-version`, `uv.lock`).
- Dependencies:
  - Runtime: `fastapi[standard]`, which includes Uvicorn and the `fastapi` CLI.
  - Dev: `pytest`, plus `httpx2`, which removes a Starlette TestClient deprecation warning.
- Added the `app/main.py` app factory (`create_app()`) and the `GET /health` route in `app/api/health.py`, which returns `{"status": "ok"}`.
- Added `tests/test_health.py`.
- Added backend setup, run, and test commands to the README.

**Why:**
- Uvicorn was chosen over Hypercorn: it is FastAPI's default and the most widely used server. HTTP/2 will be handled at the ingress, not by the app server.
- The app factory keeps tests isolated and lets settings be injected later.
- The health endpoint is the foundation for Docker health checks and Kubernetes probes.

**How to verify:**
- `cd backend && uv sync && uv run pytest -v` shows 1 passed.
- `uv run fastapi dev app/main.py`, then open `http://127.0.0.1:8000/health` and `/docs`.

**Commit:** `e1050ba`

## 2026-10-11 — Add development log

**What changed:**
- Added `DEVLOG.md`, backfilled with entries for the tasks completed so far.
- Added Working Rule 11 to `CLAUDE.md`: append a DEVLOG entry after each task.
- Updated the "Current Project Status" section of `CLAUDE.md` to reflect the work done so far.
- Listed `DEVLOG.md` in the README's structure tree.

**Why:**
- Keeps a persistent, reviewable history of what changed and why, with more detail than commit messages.
- The CLAUDE.md rule makes updating the log automatic in future sessions.

**How to verify:**
- Open `DEVLOG.md` and confirm the entries follow the format at the top of the file.
- `grep -n DEVLOG CLAUDE.md` shows the new rule.

## 2026-10-11 — Add ruff and mypy to the backend

**What changed:**
- Added dev dependencies `ruff` and `mypy`.
- Configured both in `backend/pyproject.toml`:
  - ruff: line length 88, Python 3.14 target, rule sets `E W F I B UP SIM N S RUF`. `assert` is allowed in tests.
  - mypy: `strict = true`, checks `app/` and `tests/`, with the `pydantic.mypy` plugin.
- Added lint, format, and type-check commands to the README.
- Updated the project status in `CLAUDE.md`.

**Why:**
- Catches bugs, style drift, unsafe patterns (e.g. `shell=True`), and type errors automatically instead of by eye.
- Strict mypy enforces the "use type hints" standard in `CLAUDE.md`.
- The pydantic plugin makes mypy understand Pydantic models correctly.

**How to verify:**
- `cd backend && uv sync`
- `uv run ruff check .` prints "All checks passed!"
- `uv run ruff format --check .` reports all files already formatted.
- `uv run mypy` prints "Success: no issues found".
- Optional: add `import os` to any file, and `ruff check` reports F401.

## 2026-10-11 — Separate Pydantic schemas from routers

**What changed:**
- Added the `app/schemas/` package.
- Moved `HealthResponse` from `app/api/health.py` to `app/schemas/health.py`. The router now imports it.

**Why:**
- Sets the convention before more endpoints arrive: routers (HTTP layer) live in `app/api/`, Pydantic request/response models in `app/schemas/`, one module per resource with matching names.
- Schemas can be reused by routes, services, and tests without importing router modules.

**How to verify:**
- `cd backend && uv run pytest` shows 1 passed.
- `uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` all pass.

## 2026-10-11 — Adopt standard FastAPI package layout

**What changed:**
- Moved the health router from `app/api/health.py` to `app/api/routes/health.py`.
- Added `app/core/config.py` with `APP_TITLE` and `APP_VERSION`, now used by `create_app()`.
- Added empty `app/services/` and `app/utils/` packages.
- Documented the layout conventions in `CLAUDE.md`.

**Why:**
- Follows FastAPI's official project template: `api/` holds only the HTTP layer, and `schemas/`, `services/`, `core/`, `utils/` sit beside it.
- Business logic and config are used by non-HTTP code too (future workers, ingestion, AI analysis), so they must not live under `api/`.
- Supersedes the "routers live in `app/api/`" convention from the previous entry: routers now live in `app/api/routes/`.
- Config is plain constants for now; env-based settings come later when needed.

**How to verify:**
- `cd backend && uv run pytest` shows 1 passed.
- `uv run ruff check .`, `uv run ruff format --check .`, and `uv run mypy` all pass.
- `uv run fastapi dev app/main.py`, then `curl http://127.0.0.1:8000/health` returns `{"status":"ok"}`.

## 2026-10-11 — Add GitHub Actions CI

**What changed:**
- Added `.github/workflows/ci.yml` with one `backend` job that runs on pushes to `main` and on pull requests. Steps: checkout, install uv, install Python from `.python-version`, `uv sync --locked`, `ruff check`, `ruff format --check`, `mypy`, `pytest`.
- Updated the project status in `CLAUDE.md`.

**Why:**
- Runs the same checks on every change automatically, so broken, unformatted, or badly typed code can't reach `main` unnoticed.
- Follows uv's official GitHub Actions guide.
- `uv sync --locked` fails if `uv.lock` is out of sync with `pyproject.toml`, so CI always tests the locked dependencies.
- Actions are pinned to full commit SHAs, because a tag can be repointed to different code (a supply-chain risk).
- `permissions: contents: read` gives the workflow the least access it needs.

**How to verify:**
- Locally, from `backend/`: `uv sync --locked`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, and `uv run pytest` all pass.
- After pushing, the "CI" run shows green in the repository's Actions tab.

## 2026-10-11 — Refresh README setup and run instructions

**What changed:**
- `README.md`: updated Project Status, added the `.github/` and `backend/app/` layout to Repository Structure, added uv install commands, and reorganized the Backend section into numbered steps (set up, run server, run tests, code quality, run all CI checks locally).

**Why:**
- The README still said no code existed and didn't show the backend layout.
- A new contributor (or future me) can go from clone to running server and passing checks by following one section.

**How to verify:**
- From `backend/`, run each README command as written: `uv sync`, `uv run fastapi dev app/main.py` plus `curl http://127.0.0.1:8000/health`, `uv run pytest`, and the CI-checks one-liner. All succeed.

## 2026-10-11 — Add API router aggregator

**What changed:**
- Added `app/api/main.py`, which builds `api_router` and registers each router from `app/api/routes/`.
- `app/main.py` now includes only `api_router`, not individual routers.
- Updated the layout notes in `CLAUDE.md` and the README tree.

**Why:**
- Follows the `backend/app/api/` structure of FastAPI's official full-stack template (`api/main.py` + `api/routes/`; `api/deps.py` comes later with the database).
- Adding an endpoint now only touches `app/api/`; the app factory stays unchanged.
- No URL prefix (the template uses `/api/v1`) for now, so `/health` stays at the root where probes expect it.

**How to verify:**
- `cd backend && uv run pytest` shows 1 passed; `ruff check`, `ruff format --check`, and `mypy` pass.
- `uv run fastapi dev app/main.py`, then `curl http://127.0.0.1:8000/health` returns `{"status":"ok"}`.

## 2026-10-11 — Add test coverage with pytest-cov

**What changed:**
- Added `pytest-cov` (with `coverage`) to the dev dependency group via `uv add --dev`; `uv.lock` updated.
- `backend/pyproject.toml`: new `[tool.coverage.run]`, `[tool.coverage.report]`, and `[tool.coverage.xml]` sections. They measure `app/` only with branch coverage, omit migration and generated files, show missing lines, skip empty files, fail under 80%, and write `coverage.xml`.
- `.github/workflows/ci.yml`: the test step runs `pytest --cov --cov-report=term-missing --cov-report=xml`. New steps write a Markdown coverage table to the job summary and upload `coverage.xml` as the `coverage-xml` artifact (`actions/upload-artifact`, pinned to the v7.0.1 SHA).
- `.gitignore`: added `coverage.xml`.
- README and `CLAUDE.md`: documented the coverage commands.

**Why:**
- Shows which application code is never executed by tests, and the 80% gate stops coverage from silently eroding.
- Branch coverage catches an `if` whose `else` path is never tested, which line coverage misses.
- Coverage is opt-in (`--cov`) rather than in pytest `addopts`, so running one test file locally doesn't fail the threshold. CI always runs with it.
- No external service (e.g. Codecov): the report stays in GitHub Actions (job summary + artifact), keeping with the no-third-party-services constraint.

**How to verify:**
- `cd backend && uv run pytest --cov` reports 100% and "Required test coverage of 80.0% reached".
- The full CI sequence in the README passes locally.
- The gate was tested by temporarily adding an untested module: coverage dropped to ~66% and pytest exited with code 1.
- After pushing, the CI run's summary page shows the coverage table, and `coverage-xml` appears under Artifacts.

## 2026-10-11 — Add pre-commit hooks

**What changed:**
- Added `pre-commit` to the backend dev dependency group (`uv add --dev pre-commit`); `uv.lock` updated.
- Added `.pre-commit-config.yaml` at the repo root:
  - `pre-commit-hooks` v6.0.0: trailing whitespace, end-of-file newline, YAML/TOML syntax, merge-conflict markers, large files.
  - `ruff-pre-commit` v0.17.0: `ruff-check --fix --exit-non-zero-on-fix` and `ruff-format`, limited to `backend/`.
  - `uv-pre-commit` 0.12.3: `uv lock --check --project backend` when `pyproject.toml` or `uv.lock` change.
  - Local `mypy` hook: `uv run --directory backend mypy`, so it uses the project environment and `[tool.mypy]` settings.
- README: hook install and usage instructions; `CLAUDE.md`: project status.

**Why:**
- Catches lint, format, type, and lockfile problems in seconds at commit time instead of after a push fails CI. CI stays as the backstop.
- Hook versions match the tool versions in `uv.lock`, so the hooks and CI agree.
- `--exit-non-zero-on-fix` stops the commit when ruff auto-fixes something, so fixes are reviewed and re-staged rather than slipping through silently.
- Tests are not a hook: they'd slow every commit as the suite grows, and CI runs them with coverage.

**How to verify:**
- `cd backend && uv sync && uv run pre-commit install`
- `uv run pre-commit run --all-files`: all hooks pass.
- Commit a file containing `import os` and a function returning the wrong type: the commit is blocked (ruff removes the unused import and fails; mypy reports the type error).

## 2026-10-11 — Add security scanning (Gitleaks + Trivy)

**What changed:**
- `.github/workflows/ci.yml`: new `security` job ("Security scans"), separate from the backend checks:
  - Checkout with full history (`fetch-depth: 0`) and `persist-credentials: false`.
  - Downloads the official Gitleaks v8.30.1 and Trivy v0.74.0 Linux release binaries and verifies them against SHA-256 checksums pinned in the workflow.
  - `gitleaks git . --redact`: scans every commit for secrets.
  - `trivy fs .`: scans dependencies and config files. It runs even if Gitleaks fails, so both results are always reported.
- New `trivy.yaml`: vuln + misconfig scanners (secrets are left to Gitleaks), HIGH/CRITICAL only, ignore unfixed, include dev dependencies, skip `backend/.venv`, exit code 1 on findings.
- New `.gitleaks.toml`: keeps all default rules and allowlists only `.venv/`. Without it, `gitleaks dir .` reported 8 false positives (base64 test keys in third-party packages such as dnspython and protobuf).
- README: "Security scanning" section with local install and run commands. `CLAUDE.md`: project status.

**Why:**
- Catches leaked credentials and known-vulnerable dependencies automatically, using free, open-source tools with no accounts or dashboards.
- Binaries pinned by checksum instead of `gitleaks-action` / `trivy-action`: in March 2026, attackers force-pushed malicious code to most `trivy-action` tags (CVE-2026-33634). Checksum-verified official binaries mean no third-party action code runs, and a tampered download fails the job.
- Trivy v0.74.0 rather than v0.75.0, because the newer release was only 10 days old. Both chosen versions are well after the compromised 0.69.4–0.69.6 releases.
- Only fixable HIGH/CRITICAL findings fail the build, so CI fails only on issues you can act on by upgrading.
- The workflow-level `permissions: contents: read` applies to the new job; nothing needs write access.

**How to verify:**
- Locally (checksum-verified Windows binaries of the same versions): `gitleaks git . --redact` reports "13 commits scanned, no leaks found"; `trivy fs .` loads `trivy.yaml` and reports 0 vulnerabilities in `backend/uv.lock`.
- `gitleaks dir . --redact` reports no leaks with `.gitleaks.toml`, and still flags a fake token placed in `backend/app/`.
- Negative tests in a scratch folder: a fake GitHub token makes Gitleaks exit 1 ("leaks found: 1"), and `requirements.txt` pinning `jinja2==2.10` / `requests==2.19.0` makes Trivy exit 1 (2 HIGH).
- Simulated the CI install steps: both Linux tarballs pass `sha256sum --check`, contain the expected binary, and a wrong checksum is rejected.
- After pushing, the CI run shows both "Backend checks" and "Security scans" jobs passing.

## 2026-10-12 — Environment-based settings

**What changed:**
- Declared `pydantic-settings` as a direct backend dependency. It was already installed via `fastapi[standard]`, so nothing new was downloaded.
- `app/core/config.py`: replaced the constants with a `Settings` class (`app_name`, `environment`) that reads `CLOUDOPS_*` environment variables, then `backend/.env`, then the defaults. Added `get_settings()`, cached with `lru_cache`. `APP_VERSION` stays a constant.
- `app/main.py`: `create_app(settings: Settings | None = None)` falls back to `get_settings()`. In `production`, `/docs`, `/redoc`, and `/openapi.json` are disabled.
- Added `backend/.env.example` (committed template; `.env` stays gitignored).
- Added `tests/test_config.py`: defaults, environment override, invalid value rejected, docs on in development and off in production.
- README "Configuration" notes; `CLAUDE.md` status and roadmap.

**Why:**
- The upcoming database URL and credentials must come from the environment, never from code. This sets up the mechanism first.
- Follows the FastAPI docs settings pattern (a `BaseSettings` class plus a cached getter).
- The `CLOUDOPS_` prefix avoids clashes with other tools' variables. A `Literal` type means a typo like `prodution` fails at startup instead of silently running with the wrong behaviour.
- Passing settings into `create_app()` lets tests use exact settings without touching the real environment. Tests use `_env_file=None` so a developer's `.env` can't change results.
- Disabling the interactive docs in production reduces the public attack surface.
- Agreed infrastructure direction for the next step: self-contained `infra/<service>/` folders, each with its own `compose.yaml` and README, pulled together by a root `compose.yaml` using `include`.

**How to verify:**
- `cd backend && uv run pytest --cov`: 6 passed, 100% coverage.
- `uv run fastapi dev app/main.py`: `/docs` returns 200.
- `CLOUDOPS_ENVIRONMENT=production uv run fastapi dev app/main.py`: `/docs` returns 404 and `/health` returns ok.
- `CLOUDOPS_APP_NAME` set in `backend/.env` changes the title in `/openapi.json`.
- `CLOUDOPS_ENVIRONMENT=bogus` fails at startup: "Input should be 'development', 'test' or 'production'".

## 2026-10-12 — Local PostgreSQL with Docker Compose

**What changed:**
- Added `infra/postgres/`:
  - `compose.yaml`: official `postgres:18.6-alpine` pinned by digest, credentials from `.env` (required, fails with a clear message if missing), port bound to `127.0.0.1`, `pg_isready` healthcheck, named volume `cloudops-postgres-data` mounted at `/var/lib/postgresql`.
  - `.env.example`: local-only credentials template (`.env` is gitignored).
  - `README.md`: setup, start/stop/logs, `psql` access, connection details, reset, and upgrade notes.
- Added a root `compose.yaml` that `include`s `infra/postgres/compose.yaml`.
- README: Docker is now a prerequisite, plus a "Local infrastructure" section and an updated tree. `CLAUDE.md`: the infra convention and status.

**Why:**
- The first features need a database. Docker runs the official image with no local install and identical behaviour on every machine.
- Self-contained `infra/<service>/` folders (the user's choice) keep each service's config, credentials template, and docs together. Future services (Prometheus, Loki, Tempo, ...) follow the same pattern.
- The root `compose.yaml` uses Compose `include`, so `docker compose up -d <service>` works from the root for any service, and each folder still works on its own. Compose reads each included file's `.env` from that file's own folder, per the Compose `include` reference.
- A fixed project name (`cloudops`) and a fixed volume name mean starting from the root or the folder uses the same container and data.
- Binding to localhost keeps the database off the local network. Required variables mean no credentials are hardcoded.
- PostgreSQL 18+ images store data under `/var/lib/postgresql` (PGDATA `/var/lib/postgresql/18/docker`), so the volume is mounted there; the old `/var/lib/postgresql/data` path would not persist data.
- Alpine instead of Debian: the Debian image download was repeatedly reset on this network, while the Alpine build (same PostgreSQL 18.6, smaller) downloaded fine. The only practical difference is fewer OS locales, which doesn't matter for local development.

**How to verify:**
- `cp infra/postgres/.env.example infra/postgres/.env`
- `docker compose up -d postgres`, then `docker compose ps` shows `(healthy)` and `127.0.0.1:5432->5432/tcp`.
- `docker compose exec postgres psql -U cloudops -d cloudops -c "select version();"` reports PostgreSQL 18.6.
- Persistence: created a table, ran `docker compose down` from the root and `docker compose up -d` from `infra/postgres/`, and the row was still there.
- Without `infra/postgres/.env`, `docker compose config` fails with "set POSTGRES_DB in infra/postgres/.env".
- Gitleaks and Trivy scans are clean, and the pre-commit hooks pass.

## 2026-10-12 — SQLAlchemy, Alembic, and readiness check

**What changed:**
- Dependencies: `sqlalchemy>=2.0.54,<2.1`, `psycopg[binary]>=3.3.6`, `alembic>=1.20.0`.
- Settings: `postgres_host/port/user/db` (with defaults) and a required `postgres_password` (`SecretStr`, no default). The `database_url` property is built with `URL.create()`.
- `app/core/db.py`: lazily created engine (`pool_pre_ping=True`, `connect_timeout=3`) and session factory.
- `app/api/deps.py`: `get_db()` dependency and `DbSession` type alias.
- `app/models/`: `Base` with a constraint naming convention. No tables yet.
- Alembic in `backend/alembic/` (pyproject template, config under `[tool.alembic]`, trimmed). `env.py` reads the URL from settings and accepts an existing connection (used by tests). `alembic.ini` keeps only logging config. No migration files yet.
- `GET /ready`: runs `SELECT 1`; returns 200 `{"status":"ready"}` or 503 `{"detail":"Database unavailable"}`, and logs the cause server-side. `/health` is unchanged.
- Tests:
  - `tests/conftest.py` + `tests/db.py`: switch settings to `<db>_test`, create the database if missing, drop and rebuild the schema via `alembic upgrade head` once per session, and run each test in a rolled-back transaction (`db_session`, `client` fixtures).
  - `tests/test_db.py`: correct database, migrations applied, `get_db` works, connect timeout set, rollback isolation, `/ready` 200 and 503.
  - `tests/test_config.py`: password required; URL escaping and secret masking.
  - Added `tests/__init__.py`, needed for mypy once test modules import each other.
- Ruff: allow S105/S106 (fake passwords) in `tests/` only.
- CI backend job: PostgreSQL service container (same pinned image), `CLOUDOPS_POSTGRES_*` job env, and new `alembic upgrade head` + `alembic check` steps.
- `backend/.env.example`: database settings matching `infra/postgres/.env.example`. README and `CLAUDE.md` updated.

**Why:**
- Every upcoming feature persists data through this layer. It needs to be correct, testable, and free of hardcoded credentials first.
- Sync SQLAlchemy (user's choice): simpler to write, test, and debug, and FastAPI runs sync endpoints in a thread pool. This matches FastAPI's official template.
- SQLAlchemy 2.0.x instead of 2.1: 2.1.0 was 18 days old and had four patch releases in two weeks. 2.0 is mature and maintained.
- Real PostgreSQL in tests instead of mocks: mocks can't catch SQL errors, constraint violations, or migration and model drift. Transaction rollback keeps tests isolated and fast; the `_test` database keeps dev data safe; and the "refuse non-test database" assert guards against accidents.
- The engine is created lazily, so non-DB tests and imports don't need a database.
- The constraint naming convention gives Alembic stable, predictable constraint names.
- `alembic check` in CI fails the build if someone changes a model without writing a migration.
- Liveness vs readiness: a database outage makes `/ready` fail so traffic is diverted, while `/health` stays green so healthy processes aren't restarted.
- Bug found during verification: with the database stopped, `/ready` took about 130 s to fail, because psycopg has no connect timeout by default. A 3 s `connect_timeout` brings that to about 3.2 s. A test checks the setting on a real connection and fails if the setting is removed.

**How to verify:**
- With PostgreSQL running and `backend/.env` created from the template: `uv run pytest --cov` gives 15 passed, 100% coverage.
- `uv run alembic upgrade head` and `uv run alembic check` report "No new upgrade operations detected".
- The `cloudops_test` database exists; the `cloudops` dev database has only `alembic_version`.
- With `uv run fastapi dev app/main.py` running: `/ready` returns 200. After `docker compose stop postgres`, `/ready` returns 503 in about 3 s and `/health` still returns 200. After `docker compose start postgres`, `/ready` returns 200 again.
- CI simulation (env vars only, no `.env`) passes. With no config at all, tests fail with "postgres_password Field required".
- Adding a model without a migration makes `alembic check` exit non-zero.
- Gitleaks, Trivy, and the pre-commit hooks are clean.
