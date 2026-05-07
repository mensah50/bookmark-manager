# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

A small FastAPI bookmark service deliberately built as a **sandbox for practising Claude Code configuration** (Domain 3 of the Claude Certified Architect exam). It is intentionally small but architecturally opinionated — the layering rules below exist so that `CLAUDE.md` / hooks / settings have something real to constrain.

## Hard rules — never do these

1. Never import FastAPI inside `app/services/`. Services must be framework-agnostic. Take a `Session` and Pydantic schemas in; return ORM objects out.

2. Never raise `HTTPException` from `app/services/`. Services raise domain errors from `app/core/errors.py`; routers catch and translate to HTTP responses.

3. Never return ORM objects (anything imported from `app/models/`) directly from a router. Always convert via a `_to_read()`-style helper to a Pydantic `*Read` schema first.

## Commands

```bash
pip install -r requirements.txt           # install deps
uvicorn app.main:app --reload             # run dev server (Swagger at http://localhost:8000/docs)
pytest                                    # run all tests
pytest tests/test_bookmarks.py::test_health  # run a single test
```

There is no linter or formatter configured. `pytest.ini` only sets `pythonpath = .` so tests can import `app.*`.

## Architecture & layering rules

Strict separation of concerns — these are the rules the sandbox is meant to enforce:

- **`app/routers/`** — HTTP edge only. Thin handlers that call services and translate domain exceptions to `HTTPException`. Routers may import schemas, services, and `get_db`. They should not contain business logic or query the DB directly (the `tags` router currently does, as a deliberately small exception).
- **`app/services/`** — business logic. **No FastAPI imports allowed.** Services take a `Session` and Pydantic schemas, return ORM objects, and raise domain errors from `app/core/errors.py`.
- **`app/models/`** — SQLAlchemy 2.x ORM models. `Base` lives in `app/core/database.py`; importing models there inside `init_db()` is intentional to register them with `Base.metadata` without causing circular imports.
- **`app/schemas/`** — Pydantic **v2** request/response models. Use v2 idioms: `from_attributes = True` (not `orm_mode`), `model_dump()` (not `dict()`), `HttpUrl` validation. Don't slip back into v1 patterns.
- **`app/core/`** — cross-cutting infrastructure (DB session/engine, domain error hierarchy rooted at `BookmarkError`).

### Error translation pattern

Domain errors are raised in services and caught only at the router layer:

```
service raises BookmarkNotFoundError  →  router catches  →  HTTPException(404)
service raises DuplicateBookmarkError →  router catches  →  HTTPException(409)
```

Do not raise `HTTPException` from services, and do not let SQLAlchemy `IntegrityError` leak past the service boundary (see `bookmark_service.create_bookmark` for the pattern: catch `IntegrityError`, rollback, raise domain error).

### Router → ORM → response conversion

Routers convert ORM objects to response schemas explicitly (e.g. `_to_read` in `app/routers/bookmarks.py`) because the `tags` field needs flattening from `List[Tag]` to `List[str]`. Don't return ORM objects directly when relationships need reshaping.

### Database

SQLite at `./bookmarks.db`, created on app startup via the `lifespan` handler in `main.py`. Tests call `init_db()` at import time. The session is provided per-request via the `get_db` FastAPI dependency.
