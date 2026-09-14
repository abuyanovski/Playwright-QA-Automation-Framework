import pytest

from pages.account_overview_page import AccountOverviewPage
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage


@pytest.mark.smoke
def test_customer_can_register_for_online_banking(page, base_url, customer):
    registration_page = RegistrationPage(page, base_url)
    registration_page.load()
    registration_page.register(customer)
    registration_page.expect_account_created(customer)

    account_overview_page = AccountOverviewPage(page, base_url)
    account_overview_page.open()

    assert account_overview_page.account_ids(), "Expected a new customer account"


@pytest.mark.smoke
def test_registered_customer_can_log_out_and_log_back_in(
    page, base_url, registered_customer
):
    home_page = HomePage(page, base_url)
    home_page.log_out()
    home_page.login(registered_customer.username, registered_customer.password)

    account_overview_page = AccountOverviewPage(page, base_url)
    account_overview_page.expect_loaded()
