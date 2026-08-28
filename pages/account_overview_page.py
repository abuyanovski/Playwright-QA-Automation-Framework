from playwright.sync_api import expect

from pages.base_page import BasePage


class AccountOverviewPage(BasePage):
    account_links = "#accountTable a[href*='activity.htm?id=']"

    def open(self) -> None:
        self.click_sidebar_link("Accounts Overview")
        self.expect_loaded()

    def expect_loaded(self) -> None:
        self.expect_heading("Accounts Overview")
        expect(self.page.locator("#accountTable")).to_be_visible()
        self.page.wait_for_selector(self.account_links)

    def account_ids(self) -> list[str]:
        self.expect_loaded()
        return [
            account.inner_text().strip()
            for account in self.page.locator(self.account_links).all()
        ]
