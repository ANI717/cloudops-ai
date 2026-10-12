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
