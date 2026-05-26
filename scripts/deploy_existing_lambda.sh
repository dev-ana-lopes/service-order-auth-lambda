#!/usr/bin/env bash
set -euo pipefail

LAMBDA_FUNCTION_NAME="${LAMBDA_FUNCTION_NAME:-service-order-auth-cpf}"
LAMBDA_HANDLER="${LAMBDA_HANDLER:-handler.lambda_handler}"
LAMBDA_RUNTIME="${LAMBDA_RUNTIME:-python3.12}"
LAMBDA_TIMEOUT="${LAMBDA_TIMEOUT:-15}"

bash scripts/package_lambda.sh
bash scripts/validate_lambda_package.sh

aws lambda update-function-code \
  --function-name "${LAMBDA_FUNCTION_NAME}" \
  --zip-file fileb://build/lambda.zip

aws lambda wait function-updated \
  --function-name "${LAMBDA_FUNCTION_NAME}"

aws lambda update-function-configuration \
  --function-name "${LAMBDA_FUNCTION_NAME}" \
  --runtime "${LAMBDA_RUNTIME}" \
  --handler "${LAMBDA_HANDLER}" \
  --timeout "${LAMBDA_TIMEOUT}"

aws lambda wait function-updated \
  --function-name "${LAMBDA_FUNCTION_NAME}"

aws lambda get-function-configuration \
  --function-name "${LAMBDA_FUNCTION_NAME}" \
  --query "{FunctionName:FunctionName,Runtime:Runtime,Handler:Handler,Timeout:Timeout,State:State,LastUpdateStatus:LastUpdateStatus,VpcConfig:VpcConfig}" \
  --output json
