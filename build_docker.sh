#!/usr/bin/env bash
# Build linux/amd64 image (runs on Linux / Windows / macOS Docker hosts).
set -euo pipefail
cd "$(dirname "$0")"
TAG="${1:-faceplugin/face-liveness:local}"

LIB_DRIVE="https://drive.google.com/drive/folders/1rFnw7VASLmA4q8NWenQgszFS8njRGEgt"

if [[ ! -f lib/cpu/libFaceLivenessSDK.so ]] \
  || [[ ! -f lib/cpu/libfal-eng.so ]] \
  || [[ ! -f lib/cpu/fal.fpk ]]; then
  echo "ERROR: ./lib/cpu/ is incomplete (need libFaceLivenessSDK.so, libfal-eng.so, fal.fpk)."
  echo "Download all files from Google Drive into ./lib/cpu/:"
  echo "  $LIB_DRIVE"
  exit 1
fi

docker build --platform linux/amd64 -t "$TAG" .
echo "Built $TAG (linux/amd64)"
