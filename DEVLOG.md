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
