# Bookmark Manager

A small FastAPI service for managing bookmarks with tags. Built specifically as a sandbox for practising Claude Code configuration (Domain 3 of the Claude Certified Architect exam).

This repo is both a working application *and* a teaching example. The application is deliberately small but architecturally opinionated, which gives Claude Code's configuration layers — `CLAUDE.md`, custom commands, CI workflows, and hooks — something real to constrain. If you're here to learn Claude Code configuration, jump to [Claude Code setup](#claude-code-setup) and [Learning path](#learning-path).

## Why this codebase?

It's deliberately small but architecturally opinionated. There are clear places where Claude could "go wrong" without good rules:

* Routers should stay thin — business logic belongs in `app/services/`
* Database access should never leak into routers
* Custom domain errors live in `app/core/errors.py` and get translated to HTTP at the router edge
* Pydantic v2 patterns (`from_attributes`, `model_dump`) — easy to slip back into v1

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

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/docs` for the interactive Swagger UI.

## Run tests

```
pytest
```

---

## Claude Code setup

This repo ships with a full set of Claude Code configuration, layered from "asking nicely" to "hard enforcement." Each layer is a teaching example for a different way to control Claude Code's behaviour.

### `CLAUDE.md` — project rules

At the repo root. Defines the hard rules and layering conventions Claude should follow (thin routers, framework-agnostic services, domain-error translation, Pydantic v2 idioms). This is the document Claude reads at the start of every session. It's the "asks Claude nicely" layer — usually followed, but model-decided rather than guaranteed.

### Custom commands — `.claude/commands/`

Four slash commands, each demonstrating a different concept:

| Command | What it does | Teaches |
|---------|--------------|---------|
| `/review` | Reviews a file against the CLAUDE.md rules | Read-only tools, rule cross-reference |
| `/explain` | Explains what a file does in plain English | Read-only frontmatter, structured output |
| `/test` | Writes pytest tests for a function and runs them | Arguments, refusal-on-missing, Bash lockdown |
| `/refactor` | Refactors a function while preserving behaviour | Refusal clauses, signature preservation |

Run any of them inside Claude Code by typing `/` to see the menu. They are read-only or carefully scoped — `/review` and `/explain` cannot modify files; `/test` and `/refactor` can, but with explicit refusal rules.

### CI workflows — `.github/workflows/`

Two GitHub Actions workflows that bring Claude Code into the pipeline:

* **`pr-review.yml`** — runs on every pull request. Uses headless Claude Code (`claude -p` with `--output-format json` and `--max-turns`) to review the diff, posts the findings as a PR comment, and fails the check if any *critical* issue is found (a quality gate).
* **`claude-mention.yml`** — responds to `@claude` mentions in issues and PR comments using the official `anthropics/claude-code-action`. Can implement small fixes and open PRs.

**Setup required:** both workflows need an `ANTHROPIC_API_KEY` repository secret (Settings → Secrets and variables → Actions). The mention workflow also needs the [Claude GitHub App](https://github.com/apps/claude) installed on the repo.

### Hooks — on the `hooks-demo` branch

Hooks are deterministic shell commands that fire at lifecycle points — and unlike CLAUDE.md, they're *guaranteed* to run and can *block* actions. To keep `main` clean, the hooks live on a separate branch:

```
git checkout hooks-demo
```

Then restart Claude Code so it picks up the hooks (they load at startup). The branch adds `.claude/settings.json` and `.claude/hooks/protect-files.sh`, configuring three hooks:

* a **PreToolUse** guard that blocks edits to protected files (`.env`, lock files, `.git/`) — exits 2 to block, even under `--dangerously-skip-permissions`
* a **PostToolUse** logger that records every Bash command Claude runs
* a **PostToolUse** auto-formatter that runs `black` on edited Python files

Run `/hooks` inside Claude Code to see them. Switch back with `git checkout main` to deactivate them.

---

## Learning path

The configuration above is taught in a sequence of lessons and exercises. Work through them in order — each builds on the last, and later topics (commands, CI, hooks) all depend on `CLAUDE.md` rules existing first.

1. **`/init` and authoring `CLAUDE.md`** — run `/init`, then turn the generic output into real, enforceable hard rules.
2. **Custom commands** — build `/review`, `/explain`, `/test`, and `/refactor` from scratch.
3. **CI/CD pipeline** — wire Claude Code into GitHub Actions for automated PR review and `@claude` mentions.
4. **Hooks** — add deterministic enforcement with PreToolUse and PostToolUse hooks.

Each topic has a lesson (concepts + walkthrough), an exercise (hands-on, build it yourself), and reference solutions. Attempt the exercise before looking at the solution — the learning is in the wrestling, not the reading.

### The control spectrum

A useful frame for the whole course: the four layers form a spectrum from *asking* to *enforcing*.

| Layer | Control | Guaranteed? |
|-------|---------|-------------|
| `CLAUDE.md` | Asks Claude to follow rules | No — model-decided |
| Custom commands | Package instructions + tool limits for reuse | No — model-driven once invoked |
| CI workflows | Review/act on changes outside the editor | Runs deterministically in CI |
| Hooks | Enforce policy at lifecycle points | Yes — guaranteed, can block |

A recurring exam theme: when a CLAUDE.md rule is being ignored too often, the fix is usually to move it down the spectrum — from "asked" (CLAUDE.md) to "enforced" (a PreToolUse hook).

---

## Architecture notes (for working on the app itself)

Strict separation of concerns — these are the rules the sandbox enforces:

* **`app/routers/`** — HTTP edge only. Thin handlers that call services and translate domain exceptions to `HTTPException`. May import schemas, services, and `get_db`. No business logic or direct DB queries (the `tags` router does query directly, as a deliberately small exception).
* **`app/services/`** — business logic. No FastAPI imports allowed. Takes a `Session` and Pydantic schemas, returns ORM objects, raises domain errors from `app/core/errors.py`.
* **`app/models/`** — SQLAlchemy 2.x ORM models.
* **`app/schemas/`** — Pydantic v2 request/response models (`from_attributes`, `model_dump`, `HttpUrl`).
* **`app/core/`** — cross-cutting infrastructure (DB session/engine, the domain error hierarchy rooted at `BookmarkError`).

Domain errors are raised in services and caught only at the router layer (e.g. `BookmarkNotFoundError` → `HTTPException(404)`, `DuplicateBookmarkError` → `HTTPException(409)`). See `CLAUDE.md` for the complete rule set.
