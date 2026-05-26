# Manual Lambda Validation

Use this checklist to validate `service-order-auth-cpf` in AWS Academy. Do not
commit real secrets, `tfvars`, payload files, responses or generated zip files.

## 1. Package

```bash
uv sync --locked --dev
bash scripts/package_lambda.sh
bash scripts/validate_lambda_package.sh
```

Expected package shape:

- `handler.py` at zip root
- `application/` at zip root
- `domain/` at zip root
- `infrastructure/` at zip root

## 2. Upload Code to Existing Lambda

```bash
bash scripts/deploy_existing_lambda.sh
```

The script updates code, runtime, handler and timeout only. It does not update
environment variables or VPC configuration.

## 3. Configure Environment Variables

Create a local ignored `lambda-env.json`:

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

Apply it:

```bash
aws lambda update-function-configuration \
  --function-name service-order-auth-cpf \
  --environment file://lambda-env.json
```

## 4. Configure VPC

Validated network values:

- VPC: `vpc-0580753919a62d7fa`
- Subnets: `subnet-0302bdc34eae65f23`, `subnet-0460a707dc631d61b`
- Security group: `sg-04838be5e46479e77`

Apply separately when needed:

```bash
aws lambda update-function-configuration \
  --function-name service-order-auth-cpf \
  --vpc-config SubnetIds=subnet-0302bdc34eae65f23,subnet-0460a707dc631d61b,SecurityGroupIds=sg-04838be5e46479e77
```

Confirm that the RDS security group allows this Lambda security group on port
`5432`.

## 5. Validate Configuration

```bash
aws lambda get-function-configuration \
  --function-name service-order-auth-cpf
```

Expected values:

- `Runtime`: `python3.12`
- `Handler`: `handler.lambda_handler`
- `Timeout`: `15`
- `State`: `Active`
- `LastUpdateStatus`: `Successful`
- `VpcConfig` contains the validated subnets and security group

## 6. Invoke CPF Scenarios

Invalid CPF:

```bash
CPF=00000000000 bash scripts/invoke_lambda_test.sh
```

Expected: `400 Invalid CPF`.

Valid CPF that is not registered:

```bash
CPF=12345678909 bash scripts/invoke_lambda_test.sh
```

Expected: `404 Customer not found` when this CPF is not present in the current
database.

Registered active CPF:

```bash
CPF=<registered-cpf> bash scripts/invoke_lambda_test.sh
```

Expected: `200` with a JWT response body.

## 7. Test via API Gateway

```bash
curl -i -X POST https://oubv5hamu5.execute-api.us-east-1.amazonaws.com/auth/cpf \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678909"}'
```

Expected result follows the same Lambda behavior: invalid CPF returns `400`,
valid unknown CPF returns `404`, and a registered active CPF returns `200` with
a JWT.

## Common Failures

- Database timeout: Lambda is not attached to the RDS VPC or SG rules are
  missing.
- `404 Customer not found`: CPF format is valid but customer does not exist in
  the current database.
- JWT rejected by `service-order-api`: `CUSTOMER_JWT_SECRET` or issuer differs
  between services.
- Lambda import error: package zip does not contain `handler.py` at the root.
