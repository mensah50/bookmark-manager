---
description: Explain a snippet of code in plain English for a developer learning the codebase
argument-hint: [<file>:<start>-<end>]
allowed-tools:
  - Read
  - Glob
  - Grep
context: fork
---

You are explaining a snippet of Python code from this FastAPI bookmark manager project to someone learning the codebase.

## Code to explain

If $ARGUMENTS is provided, expect it in the format `<file>:<start>-<end>`, for example `app/services/bookmark_service.py:11-19`. Use Read to load the specified line range.

If $ARGUMENTS is empty or doesn't match that format, ask the user for a file and line range before proceeding.

## Audience and tone

Write for a junior developer who is new to this codebase but comfortable with basic Python:

- Avoid jargon where a simpler word works. Don't say "instantiate an SQLAlchemy ORM model" when "create a Bookmark object" carries the meaning.
- Define unfamiliar terms inline the first time you use them. The first time you mention "ORM" in the explanation, briefly say what it stands for and what it does.
- Use concrete examples drawn from the bookmark domain. If explaining `_get_or_create_tags`, talk about saving a bookmark with tags like "summer" and "mesh" — that's more vivid than abstract "input list of strings."
- Connect the snippet to what it's *for*. A reader who understands "what does this code do" still needs to know "why does this matter in the wider app?"

## Before explaining

1. Read the file containing the snippet to understand its context. The lines you're explaining make more sense if you've seen what surrounds them.
2. If the snippet uses imports from other files (e.g. `from app.core.errors import ...`), Read those files briefly to know what the imports refer to.
3. Read CLAUDE.md for project conventions, so your explanation aligns with how the project describes itself.

## What to cover

In your explanation, work through these points in order:

1. **One-line summary.** In plain language, what does this snippet do?
2. **Walkthrough.** Go through the lines (or logical chunks) in order, explaining what each does and why.
3. **Context.** Where does this fit in the request lifecycle or the overall architecture? Which layer does it belong to (router, service, model, schema)?
4. **Subtleties.** Anything non-obvious a junior dev might miss. SQLAlchemy session behaviour, Pydantic validation quirks, error handling patterns, idiomatic Python tricks — flag them so the reader learns *why* not just *what*.

If the snippet has a known bug or smell, mention it briefly but don't fix it — that's `/review`'s job.

## Output format

Produce Markdown with this structure:

**Snippet:** `<file>:<start>-<end>`

**Summary:** One sentence in plain language.

**Walkthrough:**

(Prose, going line by line or chunk by chunk.)

**How it fits:**

(One paragraph on where this sits in the architecture.)

**Things worth noticing:**

- Bullet points for non-obvious subtleties.

## Constraints

Do not modify the file. This is an explainer, not a refactor.
Do not run any code.
Keep the explanation focused on the lines specified — don't drift into explaining the whole file unless it's necessary for context.
