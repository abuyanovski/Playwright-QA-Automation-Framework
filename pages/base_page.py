from urllib.parse import urljoin

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"

    def goto_path(self, path: str) -> None:
        self.page.goto(urljoin(self.base_url, path), wait_until="domcontentloaded")

    def click_sidebar_link(self, name: str) -> None:
        self.page.get_by_role("link", name=name).click()

    def expect_heading(self, name: str) -> None:
        expect(self.page.get_by_role("heading", name=name)).to_be_visible()
