from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol

try:
    from domain.cpf import is_valid_cpf, normalize_cpf
except ImportError:
    from ..domain.cpf import is_valid_cpf, normalize_cpf


@dataclass(frozen=True)
class CustomerRecord:
    customer_id: str
    cpf: str
    is_active: bool


class CustomerLookup(Protocol):
    def get_by_cpf(self, cpf: str) -> CustomerRecord | None:
        ...


class JwtIssuer(Protocol):
    def issue_token(self, *, cpf: str, customer_id: str) -> str:
        ...


class AuthenticateCustomerByCpf:
    def __init__(self, customer_lookup: CustomerLookup, jwt_issuer: JwtIssuer):
        self.customer_lookup = customer_lookup
        self.jwt_issuer = jwt_issuer

    def execute(self, cpf: str) -> dict:
        normalized = normalize_cpf(cpf)
        if not is_valid_cpf(normalized):
            return {"statusCode": 400, "body": {"detail": "Invalid CPF"}}

        customer = self.customer_lookup.get_by_cpf(normalized)
        if customer is None:
            return {"statusCode": 404, "body": {"detail": "Customer not found"}}

        if not customer.is_active:
            return {"statusCode": 403, "body": {"detail": "Customer is inactive"}}

        token = self.jwt_issuer.issue_token(
            cpf=normalized, customer_id=customer.customer_id
        )
        return {
            "statusCode": 200,
            "body": {
                "access_token": token,
                "token_type": "bearer",
                "expires_in": int(timedelta(minutes=60).total_seconds()),
                "issued_at": datetime.now(timezone.utc).isoformat(),
            },
        }
