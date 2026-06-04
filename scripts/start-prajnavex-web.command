#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VAULT_ROOT="$PROJECT_ROOT/vault"
URL="http://127.0.0.1:8765"
LOG_FILE="$PROJECT_ROOT/prajnavex-web.log"

cd "$PROJECT_ROOT"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  PYTHON_BIN="python"
fi

if ! curl --silent --fail --max-time 2 "$URL/api/status" >/dev/null 2>&1; then
  nohup "$PYTHON_BIN" scripts/prajnavex_web.py >"$LOG_FILE" 2>&1 &

  for _ in $(seq 1 20); do
    sleep 0.5
    if curl --silent --fail --max-time 2 "$URL/api/status" >/dev/null 2>&1; then
      break
    fi
  done
fi

open "$URL"

if [ -d "/Applications/Obsidian.app" ]; then
  open -a Obsidian "$VAULT_ROOT"
else
  open "$VAULT_ROOT"
fi
