#!/bin/bash
# protect-files.sh — PreToolUse guard that blocks edits to sensitive files.
#
# Reads the tool-call JSON from stdin, extracts the target file path, and
# exits 2 (block) if the path matches a protected pattern. Exit 2 is the ONLY
# exit code that blocks — exit 1 would merely log a warning and let the edit
# proceed. The reason written to stderr is fed back to Claude so it can adjust.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Patterns that must never be edited by Claude.
PROTECTED_PATTERNS=(".env" "package-lock.json" "poetry.lock" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'. Edit a template (e.g. .env.example) or ask a human instead." >&2
    exit 2
  fi
done

# No protected pattern matched — allow the edit. Exit 0 means "no objection";
# the normal permission flow still applies on top of this.
exit 0
