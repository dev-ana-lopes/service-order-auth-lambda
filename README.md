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
python3 -m pytest -q
```

## Deploy
- aplicar `terraform/` com `database_url`, `customer_jwt_secret` e `backend_base_url`;
- URL final esperada:
  - `POST https://<api-id>.execute-api.<region>.amazonaws.com/auth/cpf`
  - `https://<api-id>.execute-api.<region>.amazonaws.com/api/docs`

## Fallback AWS Academy
Se a conta bloquear API Gateway/Lambda, rode a função localmente via testes unitários e demonstre o fluxo com payload simulado.

## CI/CD
- lint
- unit tests
- package/zip via Terraform `archive_file`
- `terraform fmt`
- `terraform validate`

## Diagrama
Ver [docs/architecture/component-diagram.md](/mnt/c/service-order-auth-lambda/docs/architecture/component-diagram.md)
