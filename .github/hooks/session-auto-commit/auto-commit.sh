#!/usr/bin/env bash
# Session Auto-Commit Hook
# Automatically commits and pushes when a Copilot agent session ends.
# Source: adapted from github/awesome-copilot

set -euo pipefail

SKIP_AUTO_COMMIT="${SKIP_AUTO_COMMIT:-false}"

if [ "$SKIP_AUTO_COMMIT" = "true" ]; then
  echo "ℹ️ Auto-commit skipped (SKIP_AUTO_COMMIT=true)"
  exit 0
fi

# Must be inside a git repo
if ! git rev-parse --is-inside-work-tree &>/dev/null 2>&1; then
  echo "⚠️  Not inside a git repository. Skipping auto-commit."
  exit 0
fi

# Check for uncommitted changes
if [ -z "$(git status --porcelain)" ]; then
  echo "✅ No uncommitted changes. Nothing to commit."
  exit 0
fi

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

git add -A
git commit --no-verify -m "auto-commit: $TIMESTAMP"

# Attempt push — fail silently if no remote or no permission
if git push 2>/dev/null; then
  echo "✅ Auto-committed and pushed: $TIMESTAMP"
else
  echo "⚠️  Auto-committed locally but push failed. Push manually when ready."
fi
