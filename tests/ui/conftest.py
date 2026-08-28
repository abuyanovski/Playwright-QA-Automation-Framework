import pytest

from pages.registration_page import RegistrationPage
from utils.test_data import Customer, unique_customer


@pytest.fixture
def customer() -> Customer:
    return unique_customer()


@pytest.fixture
def registered_customer(page, base_url, customer: Customer) -> Customer:
    registration_page = RegistrationPage(page, base_url)
    registration_page.load()
    registration_page.register(customer)
    registration_page.expect_account_created(customer)
    return customer
