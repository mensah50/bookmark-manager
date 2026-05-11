---
description: Generate unit tests for a single function
argument-hint: [function_name]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
---

You are generating pytest unit tests for a single function in this FastAPI bookmark manager project.

## Function to test

If $ARGUMENTS is provided, treat it as the function name to test.
Otherwise, ask the user which function they want tests for before proceeding.

## Before generating tests

1. Use Grep to locate the function definition in the codebase. Confirm exactly one match. If zero or multiple matches, ask the user to disambiguate (e.g. by giving the file path).
2. Read the file containing the function to understand its signature, dependencies, and behaviour.
3. Read CLAUDE.md to load project rules.
4. Check whether a test file already exists for this module (e.g. `tests/test_bookmark_service.py` for `app/services/bookmark_service.py`).

## Test file location

Tests live in the `tests/` directory only. Never write tests anywhere else.

The test file name follows the convention `tests/test_<module>.py` where `<module>` is the source filename without extension. Examples:
- `app/services/bookmark_service.py` → `tests/test_bookmark_service.py`
- `app/routers/bookmarks.py` → `tests/test_bookmarks_router.py` (use `_router` suffix to avoid collision with the existing `tests/test_bookmarks.py` which covers integration tests)

If the target test file exists, add new test functions to it using Edit. Never modify or delete existing test functions.
If the target test file does not exist, create it using Write.

## Test design

Write tests that follow this project's existing patterns:

- Use `pytest` style (plain functions, `assert` statements, no `unittest.TestCase`).
- For services that take a database `Session`, use a fresh in-memory SQLite session per test. Reuse the helper pattern if one already exists in `tests/`; otherwise create a small `_session()` fixture at the top of the test file.
- For endpoints, use `fastapi.testclient.TestClient` as in the existing `tests/test_bookmarks.py`.
- Cover the happy path first, then at least one error path (e.g. raising the expected domain error).
- Name tests descriptively: `test_<function>_<scenario>` (e.g. `test_create_bookmark_with_new_tags`, `test_get_bookmark_raises_not_found`).

## Output format

After generating the tests, produce a short summary:

**Function tested:** `<function_name>` (in `<source_path>`)
**Test file:** `<test_file_path>` (created / extended)
**Tests added:**
- `test_<name>` — what it verifies
- `test_<name>` — what it verifies

If you needed to make assumptions about the function's intended behaviour, state them explicitly so the user can correct you.

## Constraints

Do not modify the source function under test. This is a test generator, not a refactor.
Do not modify or delete existing tests.
Do not run pytest. Generation only; running tests is the developer's job.
Only write to files inside `tests/`. Never touch source files in `app/`.
