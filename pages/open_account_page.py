from playwright.sync_api import expect

from pages.base_page import BasePage


class OpenAccountPage(BasePage):
    def open(self) -> None:
        self.click_sidebar_link("Open New Account")
        self.expect_heading("Open New Account")
        self.page.wait_for_selector("#fromAccountId option")

    def open_new_account(
        self, account_type: str = "SAVINGS", from_account_id: str | None = None
    ) -> str:
        self.page.select_option("#type", label=account_type)

        if from_account_id:
            self.page.select_option("#fromAccountId", value=from_account_id)

        self.page.get_by_role("button", name="Open New Account").click()

        self.expect_heading("Account Opened!")
        new_account_id = self.page.locator("#newAccountId")
        expect(new_account_id).to_be_visible()
        return new_account_id.inner_text().strip()
