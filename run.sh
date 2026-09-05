#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

LIB_DRIVE="https://drive.google.com/drive/folders/1rFnw7VASLmA4q8NWenQgszFS8njRGEgt"

if [[ ! -f lib/cpu/libFaceLivenessSDK.so ]]; then
  echo "ERROR: ./lib/cpu/ is empty."
  echo "Download all files from Google Drive into ./lib/cpu/:"
  echo "  $LIB_DRIVE"
  exit 1
fi

export LICENSE="${LICENSE:-$(pwd)/license.txt}"
export LD_LIBRARY_PATH="$(pwd)/lib/cpu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_PRELOAD="$(pwd)/lib/cpu/libFaceLivenessSDK.so${LD_PRELOAD:+:$LD_PRELOAD}"
export PORT="${PORT:-${FACESDK_PORT:-8084}}"
exec python3 app.py
