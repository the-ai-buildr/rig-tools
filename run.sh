#!/usr/bin/env bash
# Dev launcher for rig-tools.
# Frees port 8050 from any stale process before starting the app so reboots
# don't fail with "[Errno 98] Address already in use".
set -euo pipefail

PORT="${PORT:-8050}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Kill any process still bound to the dev port.
if pids="$(lsof -ti:"$PORT" 2>/dev/null)"; then
    if [ -n "$pids" ]; then
        echo "Freeing port $PORT (killing: $pids)"
        echo "$pids" | xargs -r kill -9
    fi
fi

# Activate the virtualenv if present.
if [ -f "$ROOT/.venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$ROOT/.venv/bin/activate"
fi

exec python app.py
