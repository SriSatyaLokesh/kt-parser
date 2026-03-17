#!/bin/bash
# Log session end event

set -euo pipefail

if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

INPUT=$(cat)
mkdir -p logs/copilot

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{\"timestamp\":\"$TIMESTAMP\",\"event\":\"sessionEnd\"}" \
  >> logs/copilot/session.log

echo "📝 Session end logged"
exit 0
