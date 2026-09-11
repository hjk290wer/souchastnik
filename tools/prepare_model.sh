#!/usr/bin/env bash
set -euo pipefail

MODEL_URL="${SOUCHASTNIK_MODEL_URL:?Set SOUCHASTNIK_MODEL_URL to the GGUF download URL}"
OUT="app/src/main/jniLibs/arm64-v8a/libmodel-qwen35-08b-q40.so"
mkdir -p "$(dirname "$OUT")"
curl -L --fail --retry 3 --retry-delay 2 "$MODEL_URL" -o "$OUT"
size="$(stat -c%s "$OUT")"
if [ "$size" -lt 100000000 ]; then
  echo "Model is unexpectedly small: $size bytes" >&2
  exit 1
fi
