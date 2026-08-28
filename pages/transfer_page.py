from decimal import Decimal

from playwright.sync_api import expect

from pages.base_page import BasePage


class TransferPage(BasePage):
    def open(self) -> None:
        self.click_sidebar_link("Transfer Funds")
        self.expect_heading("Transfer Funds")
        self.page.wait_for_selector("#fromAccountId option")
        self.page.wait_for_selector("#toAccountId option")

    def transfer(
        self,
        amount: str,
        from_account_id: str | None = None,
        to_account_id: str | None = None,
    ) -> None:
        self.page.locator("#amount").fill(amount)

        if from_account_id:
            self.page.select_option("#fromAccountId", value=from_account_id)

        if to_account_id:
            self.page.select_option("#toAccountId", value=to_account_id)

        self.page.get_by_role("button", name="Transfer").click()

    def expect_transfer_complete(
        self,
        amount: str,
        from_account_id: str | None = None,
        to_account_id: str | None = None,
    ) -> None:
        self.expect_heading("Transfer Complete!")
        expect(self.page.locator("#amountResult")).to_contain_text(
            f"${Decimal(amount):.2f}"
        )

        if from_account_id:
            expect(self.page.locator("#fromAccountIdResult")).to_contain_text(
                from_account_id
            )

        if to_account_id:
            expect(self.page.locator("#toAccountIdResult")).to_contain_text(
                to_account_id
            )
