#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT_DIR}/build/lambda-package"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

if command -v uv >/dev/null 2>&1; then
  PIP_CMD=(uv pip install --python 3.12)
else
  PIP_CMD=(python3 -m pip install)
  python3 - <<'PY'
import sys

if sys.version_info[:2] != (3, 12):
    raise SystemExit("Python 3.12 is required to build the Lambda package.")
PY
fi

"${PIP_CMD[@]}" \
  --target "${BUILD_DIR}" \
  "psycopg[binary]>=3.1.13,<4.0.0" \
  "python-jose[cryptography]>=3.3.0,<4.0.0"

cp -R "${ROOT_DIR}/src/." "${BUILD_DIR}/"
find "${BUILD_DIR}" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "${BUILD_DIR}" -type f -name "*.pyc" -delete

echo "Lambda package prepared at ${BUILD_DIR}"
