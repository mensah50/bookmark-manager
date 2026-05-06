# Bookmark Manager

A small FastAPI service for managing bookmarks with tags. Built specifically as a sandbox for practising **Claude Code configuration** (Domain 3 of the Claude Certified Architect exam).

## Why this codebase?

It's deliberately small but architecturally opinionated. There are clear places where Claude could "go wrong" without good rules:

- Routers should stay thin — business logic belongs in `app/services/`
- Database access should never leak into routers
- Custom domain errors live in `app/core/errors.py` and get translated to HTTP at the router edge
- Pydantic v2 patterns (`from_attributes`, `model_dump`) — easy to slip back into v1

That gives your `CLAUDE.md` rules something real to constrain.

## Layout

```
app/
├── main.py              # FastAPI entrypoint
├── core/                # Cross-cutting infra (DB, errors)
├── models/              # SQLAlchemy ORM models
├── schemas/             # Pydantic request/response schemas
├── services/            # Business logic — no FastAPI imports allowed
└── routers/             # HTTP edge — thin, delegate to services
tests/
└── test_bookmarks.py
```

## Run it

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/docs` for the interactive Swagger UI.

## Run tests

```bash
pytest
```
