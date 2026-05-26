# service-order-auth-lambda

Serverless CPF authentication function for Phase 3. This repository owns only
the Lambda implementation, package, validation scripts and reference Terraform.
Responsibilities must not be moved to `service-order-api`.

## Validated AWS State

- Lambda function: `service-order-auth-cpf`
- Runtime: Python 3.12
- Handler: `handler.lambda_handler`
- Timeout: 15 seconds
- API Gateway route: `POST /auth/cpf`
- Validated invalid CPF response: `400 Invalid CPF`
- Validated existing-format but unknown CPF response: `404 Customer not found`

The Lambda was created manually in AWS Academy with `LabRole`. Automated
Terraform apply remains disabled because the manually created resources are not
imported into remote state.

## Runtime and Package

```bash
uv sync --locked --dev
bash scripts/package_lambda.sh
bash scripts/validate_lambda_package.sh
```

The package script creates `build/lambda.zip`. The zip must contain
`handler.py`, `application/`, `domain/` and `infrastructure/` at the zip root.
The `build/` directory is ignored by Git.

## Manual Deploy to Existing Lambda

Use this only from a local machine or controlled shell with AWS credentials.
The script updates code, runtime, handler and timeout. It intentionally does
not update environment variables or VPC settings.

```bash
bash scripts/deploy_existing_lambda.sh
```

Defaults:

- `LAMBDA_FUNCTION_NAME=service-order-auth-cpf`
- `LAMBDA_HANDLER=handler.lambda_handler`
- `LAMBDA_RUNTIME=python3.12`
- `LAMBDA_TIMEOUT=15`

## Environment Variables

Configure secrets separately. Do not use inline commands with real secrets in
shell history. Prefer a local ignored file named `lambda-env.json`:

```json
{
  "Variables": {
    "DATABASE_URL": "postgresql://user:password@host:5432/service_order_db?sslmode=require",
    "CUSTOMER_JWT_SECRET": "same-secret-used-by-service-order-api",
    "CUSTOMER_JWT_ISSUER": "service-order-auth-lambda/production",
    "CUSTOMER_JWT_ALGORITHM": "HS256"
  }
}
```

Apply it manually:

```bash
aws lambda update-function-configuration \
  --function-name service-order-auth-cpf \
  --environment file://lambda-env.json
```

`lambda-env.json` is local only and ignored by Git.

## VPC Configuration

The Lambda must be attached to the RDS VPC to avoid database timeouts.

Validated values:

- VPC: `vpc-0580753919a62d7fa`
- Subnets:
  - `subnet-0302bdc34eae65f23`
  - `subnet-0460a707dc631d61b`
- Security group: `sg-04838be5e46479e77`

The security group must be allowed by the RDS security group on port `5432`.
Run the VPC update separately when needed; it is not part of the deploy script.

```bash
aws lambda update-function-configuration \
  --function-name service-order-auth-cpf \
  --vpc-config SubnetIds=subnet-0302bdc34eae65f23,subnet-0460a707dc631d61b,SecurityGroupIds=sg-04838be5e46479e77
```

Validate configuration:

```bash
aws lambda get-function-configuration \
  --function-name service-order-auth-cpf
```

## Invoke Tests

```bash
CPF=00000000000 bash scripts/invoke_lambda_test.sh
CPF=12345678909 bash scripts/invoke_lambda_test.sh
CPF=<registered-cpf> bash scripts/invoke_lambda_test.sh
```

Expected results:

- Invalid CPF: `400 Invalid CPF`
- Valid CPF not found in database: `404 Customer not found`
- Registered active CPF: `200` with JWT payload

API Gateway smoke test:

```bash
curl -i -X POST https://oubv5hamu5.execute-api.us-east-1.amazonaws.com/auth/cpf \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678909"}'
```

## Terraform

Terraform is kept as reference IaC for accounts with full permissions or for a
future import of the manually created resources into remote state. Do not run
`terraform apply` in this AWS Academy setup.

Safe validation:

```bash
bash scripts/package_lambda.sh
bash scripts/validate_lambda_package.sh
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate
terraform -chdir=terraform plan -input=false \
  -var="database_url=postgresql://user:pass@example.com:5432/db?sslmode=require" \
  -var="customer_jwt_secret=fake-secret-value-with-32-characters" \
  -var="backend_base_url=https://backend.example.com" \
  -var='private_subnet_ids=["subnet-00000000000000000","subnet-11111111111111111"]' \
  -var='lambda_security_group_ids=["sg-00000000000000000"]' || true
```

The plan remains non-blocking because this repository represents manual lab
resources that are not imported into remote state.

## CI/CD

The workflow validates formatting, imports, lint, tests, Lambda package shape
and Terraform syntax. The manual deploy job only documents the AWS Academy
workaround and does not use AWS credentials, upload code or run `terraform
apply`.

## Local Quality Checks

```bash
uv sync --locked --dev
uv run black --check src tests
uv run isort --check-only src tests
uv run flake8 src tests
uv run pytest -q
```

## Documentation

- `docs/runbooks/aws-academy-lambda-limitation.md`
- `docs/runbooks/manual-lambda-validation.md`
