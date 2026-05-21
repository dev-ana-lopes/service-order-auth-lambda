import json

from jose import jwt

from src.application.authenticate_customer_by_cpf import (
    AuthenticateCustomerByCpf,
    CustomerRecord,
)
from src.handler import lambda_handler
from src.infrastructure.jwt_issuer import JwtIssuer


class FakeLookup:
    def __init__(self, customer=None):
        self.customer = customer

    def get_by_cpf(self, cpf: str):
        return self.customer


def test_invalid_cpf_returns_400():
    use_case = AuthenticateCustomerByCpf(FakeLookup(), JwtIssuer(secret="secret" * 8))
    result = use_case.execute("123")
    assert result["statusCode"] == 400


def test_customer_not_found_returns_404():
    use_case = AuthenticateCustomerByCpf(FakeLookup(), JwtIssuer(secret="secret" * 8))
    result = use_case.execute("11144477735")
    assert result["statusCode"] == 404


def test_inactive_customer_returns_403():
    use_case = AuthenticateCustomerByCpf(
        FakeLookup(CustomerRecord(customer_id="1", cpf="11144477735", is_active=False)),
        JwtIssuer(secret="secret" * 8),
    )
    result = use_case.execute("11144477735")
    assert result["statusCode"] == 403


def test_active_customer_returns_token():
    issuer = JwtIssuer(secret="secret" * 8, issuer="service-order-auth-lambda/test")
    use_case = AuthenticateCustomerByCpf(
        FakeLookup(CustomerRecord(customer_id="1", cpf="11144477735", is_active=True)),
        issuer,
    )
    result = use_case.execute("11144477735")
    assert result["statusCode"] == 200
    token = result["body"]["access_token"]
    payload = jwt.get_unverified_claims(token)
    assert payload["sub"] == "11144477735"
    assert payload["customer_id"] == "1"
    assert payload["role"] == "customer"
    assert payload["iss"] == "service-order-auth-lambda/test"


def test_lambda_handler_wraps_json_response(monkeypatch):
    monkeypatch.setattr(
        "src.handler.PostgresCustomerLookup",
        lambda: FakeLookup(
            CustomerRecord(customer_id="1", cpf="11144477735", is_active=True)
        ),
    )
    monkeypatch.setattr(
        "src.handler.JwtIssuer",
        lambda: JwtIssuer(secret="secret" * 8, issuer="service-order-auth-lambda/test"),
    )
    response = lambda_handler({"body": json.dumps({"cpf": "111.444.777-35"})}, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["token_type"] == "bearer"
