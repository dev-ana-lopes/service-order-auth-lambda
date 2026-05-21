from __future__ import annotations

import os

import psycopg

try:
    from application.authenticate_customer_by_cpf import CustomerRecord
except ImportError:
    from ..application.authenticate_customer_by_cpf import CustomerRecord

_CONNECTION = None


class PostgresCustomerLookup:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.environ["DATABASE_URL"]

    def _get_connection(self):
        global _CONNECTION
        if _CONNECTION is None or _CONNECTION.closed:
            _CONNECTION = psycopg.connect(self.database_url)
        return _CONNECTION

    def get_by_cpf(self, cpf: str) -> CustomerRecord | None:
        with self._get_connection().cursor() as cursor:
            cursor.execute(
                "SELECT id::text, cpf_cnpj, is_active FROM customers WHERE cpf_cnpj = %s LIMIT 1",
                (cpf,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return CustomerRecord(customer_id=row[0], cpf=row[1], is_active=bool(row[2]))
