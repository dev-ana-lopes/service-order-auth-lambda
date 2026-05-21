from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from jose import jwt


class JwtIssuer:
    def __init__(
        self,
        secret: str | None = None,
        issuer: str | None = None,
        algorithm: str | None = None,
        expiration_minutes: int | None = None,
    ):
        self.secret = secret or os.environ["CUSTOMER_JWT_SECRET"]
        self.issuer = issuer or os.environ.get(
            "CUSTOMER_JWT_ISSUER", "service-order-auth-lambda/development"
        )
        self.algorithm = algorithm or os.environ.get("CUSTOMER_JWT_ALGORITHM", "HS256")
        self.expiration_minutes = expiration_minutes or int(
            os.environ.get("CUSTOMER_JWT_EXPIRATION_MINUTES", "60")
        )

    def issue_token(self, *, cpf: str, customer_id: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=self.expiration_minutes
        )
        payload = {
            "sub": cpf,
            "customer_id": customer_id,
            "role": "customer",
            "iss": self.issuer,
            "exp": expires_at,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
