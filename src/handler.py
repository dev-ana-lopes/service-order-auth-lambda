from __future__ import annotations

import json

from .application.authenticate_customer_by_cpf import AuthenticateCustomerByCpf
from .infrastructure.jwt_issuer import JwtIssuer
from .infrastructure.postgres_customer_lookup import PostgresCustomerLookup



def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }



def lambda_handler(event, context):
    del context
    body = event.get("body") or "{}"
    if isinstance(body, str):
        payload = json.loads(body)
    else:
        payload = body

    use_case = AuthenticateCustomerByCpf(PostgresCustomerLookup(), JwtIssuer())
    result = use_case.execute(payload.get("cpf", ""))
    return _response(result["statusCode"], result["body"])
