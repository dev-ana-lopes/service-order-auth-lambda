#!/usr/bin/env bash
set -euo pipefail

LAMBDA_FUNCTION_NAME="${LAMBDA_FUNCTION_NAME:-service-order-auth-cpf}"
CPF="${CPF:-12345678909}"
PAYLOAD_FILE="$(mktemp)"
RESPONSE_FILE="$(mktemp)"

cleanup() {
  rm -f "${PAYLOAD_FILE}" "${RESPONSE_FILE}"
}
trap cleanup EXIT

printf '{"body":"{\"cpf\":\"%s\"}"}' "${CPF}" > "${PAYLOAD_FILE}"

aws lambda invoke \
  --function-name "${LAMBDA_FUNCTION_NAME}" \
  --payload "fileb://${PAYLOAD_FILE}" \
  "${RESPONSE_FILE}" >/dev/null

cat "${RESPONSE_FILE}"
echo
