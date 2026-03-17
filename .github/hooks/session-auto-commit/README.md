---
name: 'Session Auto-Commit'
description: 'Automatically commits and pushes changes when a Copilot agent session ends'
tags: ['automation', 'git', 'productivity']
---

# Session Auto-Commit Hook

Automatically commits and pushes an uncommitted changes when a Copilot coding agent session ends.
Prevents losing work from a background agent session.

## Installation

```bash
cp -r .github/hooks/session-auto-commit /path/to/your-project/.github/hooks/
chmod +x .github/hooks/session-auto-commit/auto-commit.sh
git add .github/hooks/ && git commit -m "chore: add session-auto-commit hook" && git push
```

## Disable for a Session

```bash
export SKIP_AUTO_COMMIT=true
```

## Commit Format

```
auto-commit: YYYY-MM-DD HH:MM:SS UTC
```

## Source

Adapted from [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/hooks/session-auto-commit)
