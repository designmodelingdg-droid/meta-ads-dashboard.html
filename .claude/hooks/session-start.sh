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

# Skill video-pizarra: ffmpeg para el render, numpy y Pillow para la mezcla de audio y las capturas.
if ! command -v ffmpeg &>/dev/null; then
  (apt-get update -qq && apt-get install -y -qq --no-install-recommends ffmpeg) >/dev/null 2>&1 || true
fi
if ! python3 -c "import numpy, PIL" &>/dev/null; then
  pip install -q numpy pillow >/dev/null 2>&1 || true
fi
