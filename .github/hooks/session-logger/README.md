---
name: 'Session Logger'
description: 'Logs all Copilot coding agent session activity for audit and analysis'
tags: ['logging', 'audit', 'analytics']
---

# Session Logger Hook

Logs every Copilot agent session start, end, and user prompt submission to local JSON files.
Useful for team audit trails and understanding how developers use Copilot.

## What Gets Logged

| Event | Log File | What it records |
|-------|---------|----------------|
| Session start | `logs/copilot/session.log` | Timestamp + working directory |
| Session end | `logs/copilot/session.log` | Timestamp |
| Every prompt | `logs/copilot/prompts.log` | Timestamp + log level |

> **Privacy**: Full prompt text is never logged — only event metadata.

## Installation

```bash
cp -r .github/hooks/session-logger /path/to/your-project/.github/hooks/
chmod +x .github/hooks/session-logger/*.sh
mkdir -p logs/copilot
echo "logs/" >> .gitignore
git add .github/hooks/ .gitignore && git commit -m "chore: add session-logger hook" && git push
```

## Log Format

`logs/copilot/session.log` (JSON Lines):
```json
{"timestamp":"2026-03-02T16:00:00Z","event":"sessionStart","cwd":"/workspace/project"}
{"timestamp":"2026-03-02T16:45:00Z","event":"sessionEnd"}
```

`logs/copilot/prompts.log` (JSON Lines):
```json
{"timestamp":"2026-03-02T16:01:00Z","event":"userPromptSubmitted","level":"INFO"}
{"timestamp":"2026-03-02T16:15:00Z","event":"userPromptSubmitted","level":"INFO"}
```

## Disable

```bash
export SKIP_LOGGING=true
```

## Requirements

- `jq` installed (for session start JSON encoding)
- `bash` 4+

## Source

Adapted from [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/hooks/session-logger)
