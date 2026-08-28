from decimal import Decimal

from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.test_data import Payee


class BillPayPage(BasePage):
    def open(self) -> None:
        self.click_sidebar_link("Bill Pay")
        self.expect_heading("Bill Payment Service")
        self.page.wait_for_selector("input[name='payee.name']")

    def pay_bill(
        self, payee: Payee, amount: str, from_account_id: str | None = None
    ) -> None:
        self.page.locator("input[name='payee.name']").fill(payee.name)
        self.page.locator("input[name='payee.address.street']").fill(payee.street)
        self.page.locator("input[name='payee.address.city']").fill(payee.city)
        self.page.locator("input[name='payee.address.state']").fill(payee.state)
        self.page.locator("input[name='payee.address.zipCode']").fill(payee.zip_code)
        self.page.locator("input[name='payee.phoneNumber']").fill(payee.phone)
        self.page.locator("input[name='payee.accountNumber']").fill(payee.account_number)
        self.page.locator("input[name='verifyAccount']").fill(payee.account_number)
        self.page.locator("input[name='amount']").fill(amount)

        if from_account_id:
            self.page.select_option("select[name='fromAccountId']", value=from_account_id)

        self.page.get_by_role("button", name="Send Payment").click()

    def expect_payment_complete(self, payee: Payee, amount: str) -> None:
        self.expect_heading("Bill Payment Complete")
        result = self.page.locator("#billpayResult")
        expect(result).to_contain_text(payee.name)
        expect(result).to_contain_text(f"${Decimal(amount):.2f}")
