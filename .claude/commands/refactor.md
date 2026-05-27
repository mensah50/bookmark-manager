---
description: Refactor a single function with a stated reason
argument-hint: <function_name> "<reason>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Bash
context: fork
---

You are refactoring a single Python function in this FastAPI bookmark manager project.

## Required arguments

This command requires two arguments:

1. A function name (the first word in $ARGUMENTS).
2. A reason, enclosed in double quotes (the rest of $ARGUMENTS).

If either argument is missing, refuse to proceed. Tell the user the correct format and stop. Do not guess at the reason or pick a function to refactor on their behalf.

Example of a valid invocation: `/refactor _get_or_create_tags "deduplicate input names before querying to avoid the IntegrityError race"`

## Before refactoring

1. Use Grep to locate the function definition. If there is not exactly one match, ask the user to disambiguate by giving a file path.
2. Read the file containing the function.
3. Read CLAUDE.md to load project rules and hard constraints.
4. Identify every call site of the function using Grep, so you understand the function's contract (what its callers expect).

## Refusal clauses

You must refuse and explain (do not edit) if any of the following apply:

- The reason describes a refactor that would violate any rule in CLAUDE.md's "Hard rules — never do these" section.
- The refactor would change the function's public signature (parameter names, parameter order, parameter types, or return type), unless the user's reason explicitly says they want a signature change.
- The refactor would require changes to other files. This command refactors one function in place; cross-file changes are out of scope.
- The function does not exist or you cannot uniquely identify it.

If you refuse, explain which rule was violated and suggest what the user could do instead.

## Refactoring

If the request passes the checks above:

1. Make the change using Edit. Modify only the body of the function — do not touch other functions in the file, imports the function doesn't use, or unrelated code.
2. Preserve the function's docstring if it has one; update it only if the user's reason explicitly requires it.
3. Preserve the function's behaviour. The refactor should be a transformation, not a rewrite.

## Verification

After editing, run the test suite to confirm behaviour is preserved.

Use Bash to run **only this exact command**:

pytest -q

Do not run any other shell command under any circumstances. Do not chain commands with `&&`, `;`, or `|`. Do not invoke `bash`, `sh`, `python`, `pip`, `git`, or anything other than `pytest -q`. If pytest is not the right verification step for some reason, stop and tell the user — do not improvise.

Report the test result clearly:

- If all tests pass: state that verification succeeded.
- If any test fails: state which test failed and quote the failure message. Do not attempt to "fix" the failing test by editing it. The failure is a signal that the refactor changed behaviour, and the user needs to decide what to do.

## Output format

Produce Markdown with this structure:

**Function refactored:** `<function_name>` (in `<source_path>`)

**Reason:** "<reason as given>"

**What changed:**

A short, junior-dev-readable explanation of the transformation. Avoid jargon; use bookmark-domain examples where they help.

**Before:**

(original function body in a code block)

**After:**

(refactored function body in a code block)

**Verification:**

State the test result. If failed, quote the failure.

**To undo:**

`git checkout <source_path>`

## Constraints

Do not create new files. This command modifies one existing function only.
Do not modify any file other than the one containing the function.
Do not modify tests.
Do not run any shell command other than `pytest -q`.
Do not change the function's public signature unless explicitly requested.
