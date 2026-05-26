#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT_DIR}/build/lambda-package"
ZIP_PATH="${ROOT_DIR}/build/lambda.zip"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
rm -f "${ZIP_PATH}"

if command -v uv >/dev/null 2>&1; then
  UV_BIN="$(command -v uv)"
elif [ -x /snap/bin/uv ]; then
  UV_BIN="/snap/bin/uv"
else
  UV_BIN=""
fi

if [ -n "${UV_BIN}" ]; then
  PIP_CMD=("${UV_BIN}" pip install --python 3.12)
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

python3 - "${BUILD_DIR}" "${ZIP_PATH}" <<'PY'
from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

package_dir = Path(sys.argv[1])
zip_path = Path(sys.argv[2])

with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
    for directory in sorted(path for path in package_dir.rglob("*") if path.is_dir()):
        archive.writestr(f"{directory.relative_to(package_dir).as_posix()}/", "")
    for file_path in sorted(path for path in package_dir.rglob("*") if path.is_file()):
        archive.write(file_path, file_path.relative_to(package_dir).as_posix())
PY

echo "Lambda package created at ${ZIP_PATH}"
