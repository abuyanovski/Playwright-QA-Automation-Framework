import pytest

from pages.account_overview_page import AccountOverviewPage
from pages.bill_pay_page import BillPayPage
from pages.open_account_page import OpenAccountPage
from pages.transfer_page import TransferPage
from utils.test_data import sample_payee


@pytest.mark.regression
def test_customer_can_open_a_savings_account(page, base_url, registered_customer):
    account_overview_page = AccountOverviewPage(page, base_url)
    account_overview_page.open()
    original_accounts = account_overview_page.account_ids()

    open_account_page = OpenAccountPage(page, base_url)
    open_account_page.open()
    new_account_id = open_account_page.open_new_account(
        account_type="SAVINGS",
        from_account_id=original_accounts[0],
    )

    assert new_account_id not in original_accounts


@pytest.mark.regression
def test_customer_can_transfer_funds_between_accounts(
    page, base_url, registered_customer
):
    account_overview_page = AccountOverviewPage(page, base_url)
    account_overview_page.open()
    from_account_id = account_overview_page.account_ids()[0]

    open_account_page = OpenAccountPage(page, base_url)
    open_account_page.open()
    to_account_id = open_account_page.open_new_account(
        account_type="SAVINGS",
        from_account_id=from_account_id,
    )

    transfer_page = TransferPage(page, base_url)
    transfer_page.open()
    transfer_page.transfer(
        amount="25.00",
        from_account_id=from_account_id,
        to_account_id=to_account_id,
    )
    transfer_page.expect_transfer_complete(
        amount="25.00",
        from_account_id=from_account_id,
        to_account_id=to_account_id,
    )


@pytest.mark.regression
def test_customer_can_pay_a_bill(page, base_url, registered_customer):
    account_overview_page = AccountOverviewPage(page, base_url)
    account_overview_page.open()
    from_account_id = account_overview_page.account_ids()[0]

    payee = sample_payee()
    bill_pay_page = BillPayPage(page, base_url)
    bill_pay_page.open()
    bill_pay_page.pay_bill(payee=payee, amount="15.25", from_account_id=from_account_id)
    bill_pay_page.expect_payment_complete(payee=payee, amount="15.25")
