---
description: Review the current file for bugs, style issues, and rule violations
argument-hint: [file_path]
allowed-tools:
  - Read
  - Glob
  - Grep
---

You are reviewing Python code in this FastAPI bookmark manager project.

## File to review

If $ARGUMENTS is provided, review that file.
Otherwise, ask the user which file they want reviewed before proceeding.

## What to check

Review the file against these criteria, in this order of importance:

1. **CLAUDE.md hard rules.** Read CLAUDE.md and confirm the file does not violate any rule in the "Hard rules — never do these" section. Flag any violation as **Critical**.

2. **Architectural layering.** Confirm the file respects its layer's boundaries:
   - Routers must not query the database or import from `app/models/` directly
   - Services must not import FastAPI or raise HTTPException
   - Models should contain only ORM definitions, not business logic

3. **Pydantic v2 idioms.** Flag any v1 patterns (`Config.orm_mode`, `.dict()`, `.parse_obj()`).

4. **Bugs and correctness.** Logic errors, off-by-one issues, incorrect error handling, missing await on async calls.

5. **Style and clarity.** Unclear names, dead code, inconsistent formatting, missing type hints on public functions.

## Output format

Produce a Markdown report with this structure:

**File reviewed:** `<path>`

**Summary:** One sentence overall verdict.

**Issues found:**

For each issue:
- **Severity:** Critical / High / Medium / Low
- **Location:** Line number or function name
- **Issue:** What's wrong
- **Suggestion:** How to fix it (do not write the fix; describe it)

If no issues are found, say so explicitly.

## Constraints

Do not modify the file. This is a review, not a refactor.
Do not run any code or shell commands.
If you need to look at related files (e.g. CLAUDE.md, or another file the reviewed file imports from), use Read — but keep the review focused on the target file.
