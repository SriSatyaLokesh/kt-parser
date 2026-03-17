#!/bin/bash
# Log user prompt submission

set -euo pipefail

if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

INPUT=$(cat)
mkdir -p logs/copilot

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{\"timestamp\":\"$TIMESTAMP\",\"event\":\"userPromptSubmitted\",\"level\":\"${LOG_LEVEL:-INFO}\"}" \
  >> logs/copilot/prompts.log

exit 0
