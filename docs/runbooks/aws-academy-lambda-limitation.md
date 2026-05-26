# AWS Academy Lambda Limitation and Workaround

## Context

During Phase 3 validation, automated Lambda creation through Terraform/CLI hit
an AWS Academy/Vocareum permission limitation. This does not mean the Lambda
could not exist. It means automated creation/apply was not a reliable path in
the lab account.

The validated Lambda is `service-order-auth-cpf`.

## Validated Workaround

The function was created manually in the AWS Console using `LabRole`. The code
still belongs to this repository and was packaged locally:

```bash
bash scripts/package_lambda.sh
bash scripts/validate_lambda_package.sh
```

The generated artifact was uploaded to the existing function:

```bash
aws lambda update-function-code \
  --function-name service-order-auth-cpf \
  --zip-file fileb://build/lambda.zip
```

The function configuration was validated with:

- Runtime: `python3.12`
- Handler: `handler.lambda_handler`
- Timeout: `15`
- API Gateway route: `POST /auth/cpf`

## VPC Requirement

The Lambda timed out until it was associated with the RDS VPC. VPC attachment
is a separate manual/CLI operation and is not run by the repository deploy
script.

Validated values:

- VPC: `vpc-0580753919a62d7fa`
- Subnets: `subnet-0302bdc34eae65f23`, `subnet-0460a707dc631d61b`
- Security group: `sg-04838be5e46479e77`

Validated command shape:

```bash
aws lambda update-function-configuration \
  --function-name service-order-auth-cpf \
  --vpc-config SubnetIds=subnet-0302bdc34eae65f23,subnet-0460a707dc631d61b,SecurityGroupIds=sg-04838be5e46479e77
```

The RDS security group must allow this Lambda security group on port `5432`.

## Terraform Status

Terraform remains a reference IaC implementation for a regular AWS account or
for a future import of the manually created resources into remote state. In the
AWS Academy lab, `terraform apply` stays disabled.

The CI validates Terraform syntax and keeps `terraform plan` non-blocking with
fake values because the real resources are manual and not imported into remote
state.

## What This Repository Provides

- CPF authentication Lambda implementation.
- Unit tests for business behavior.
- Package and package validation scripts.
- Manual deploy script for an existing Lambda.
- Reference Terraform for Lambda/API Gateway/VPC configuration.
- Runbooks for manual validation in AWS Academy.
