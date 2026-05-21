# service-order-auth-lambda

Autenticação serverless por CPF para a Fase 3 do Tech Challenge FIAP.

## O que faz
- expõe `POST /auth/cpf` via API Gateway HTTP API;
- valida CPF;
- consulta `customers` no PostgreSQL;
- exige `is_active=true`;
- emite JWT com `sub`, `customer_id`, `role`, `exp`, `iss`.

## Execução local
```bash
uv sync --locked --dev
uv run pytest -q
```

## Package local
```bash
bash scripts/package_lambda.sh
```

O pacote é criado em `build/lambda-package` com código e dependências de runtime. O diretório `build/` é ignorado pelo Git.

## Deploy
- copie `terraform/terraform.tfvars.example` para `terraform/terraform.tfvars` apenas no ambiente local;
- preencha `database_url`, `customer_jwt_secret` e `backend_base_url` com valores reais locais ou secrets de CI;
- execute `bash scripts/package_lambda.sh` antes de `terraform plan/apply`;
- aplique `terraform/`;
- URL final esperada:
  - `POST https://<api-id>.execute-api.<region>.amazonaws.com/auth/cpf`
  - `https://<api-id>.execute-api.<region>.amazonaws.com/api/docs`

## Fallback AWS Academy
Se a conta bloquear API Gateway/Lambda, rode a função localmente via testes unitários e demonstre o fluxo com payload simulado.

## CI/CD
- lint
- unit tests
- package com dependências via `scripts/package_lambda.sh`
- `terraform fmt`
- `terraform validate`
- `terraform plan`

O deploy via workflow fica restrito a `workflow_dispatch` e environment protegido.

## Secrets e variáveis
- `DATABASE_URL` e `CUSTOMER_JWT_SECRET` são sensíveis.
- Nunca versionar `terraform.tfvars`, `.env`, zips ou diretórios `build/`.
- A Lambda não deve logar CPF completo, tokens ou strings de conexão.

## Checklist de validação
- `uv sync --locked --dev`
- `uv run python -m compileall src tests`
- `uv run pytest -q`
- `bash scripts/package_lambda.sh`
- `terraform -chdir=terraform fmt -check -recursive`
- `terraform -chdir=terraform init -backend=false`
- `terraform -chdir=terraform validate`

## Diagrama
Ver [docs/architecture/component-diagram.md](/mnt/c/service-order-auth-lambda/docs/architecture/component-diagram.md)
