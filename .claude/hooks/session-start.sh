#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Plain HTML project — no package installs needed.
# Ensure htmlhint is available for linting if Node is present.
if command -v npm &>/dev/null && ! command -v htmlhint &>/dev/null; then
  npm install -g htmlhint --prefer-offline 2>/dev/null || true
fi
