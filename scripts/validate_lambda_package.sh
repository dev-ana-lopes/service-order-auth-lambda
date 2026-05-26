#!/usr/bin/env bash
set -euo pipefail

ZIP_PATH="${1:-build/lambda.zip}"

test -f "${ZIP_PATH}"

ZIP_NAMES="$(unzip -Z1 "${ZIP_PATH}")"

printf '%s\n' "${ZIP_NAMES}" | grep -qx "handler.py"
printf '%s\n' "${ZIP_NAMES}" | grep -qx "application/"
printf '%s\n' "${ZIP_NAMES}" | grep -qx "domain/"

echo "Lambda package is valid: ${ZIP_PATH}"
