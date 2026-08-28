from dataclasses import dataclass
from datetime import datetime, timezone
import secrets


@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    ssn: str
    username: str
    password: str


@dataclass(frozen=True)
class Payee:
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    account_number: str


def unique_customer() -> Customer:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    suffix = secrets.token_hex(3)

    return Customer(
        first_name="Alex",
        last_name="Portfolio",
        street="100 Automation Way",
        city="Los Angeles",
        state="CA",
        zip_code="90001",
        phone="5551234567",
        ssn=f"{secrets.randbelow(9000) + 1000}",
        username=f"qa{timestamp}{suffix}",
        password="Passw0rd123",
    )


def sample_payee() -> Payee:
    account_number = f"88{secrets.randbelow(10_000_000):07d}"

    return Payee(
        name="Portfolio Utilities",
        street="501 Billing Lane",
        city="Pasadena",
        state="CA",
        zip_code="91101",
        phone="5559876543",
        account_number=account_number,
    )
