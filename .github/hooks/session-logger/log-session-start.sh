#!/bin/bash
# Log session start event

set -euo pipefail

if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

INPUT=$(cat)
mkdir -p logs/copilot

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CWD=$(pwd)

jq -Rn --arg timestamp "$TIMESTAMP" --arg cwd "$CWD" \
  '{"timestamp":$timestamp,"event":"sessionStart","cwd":$cwd}' \
  >> logs/copilot/session.log

echo "📝 Session start logged"
exit 0
