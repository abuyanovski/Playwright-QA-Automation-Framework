from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def load(self) -> None:
        self.goto_path("index.htm")
        expect(self.page.locator("#loginPanel")).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.page.locator("input[name='username']").fill(username)
        self.page.locator("input[name='password']").fill(password)
        self.page.locator("input[value='Log In']").click()

    def log_out(self) -> None:
        self.page.get_by_role("link", name="Log Out").click()
        expect(self.page.locator("#loginPanel")).to_be_visible()
