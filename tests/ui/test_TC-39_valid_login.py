import json
from pathlib import Path

from playwright.sync_api import Page, expect


def test_TC39_valid_login(page: Page) -> None:
    credentials_path = Path(__file__).resolve().parents[2] / "data" / "active_user.json"
    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    expect(page.get_by_role("img", name="ParaBank")).to_be_visible()
    page.locator('input[name="username"]').fill(credentials["username"])
    page.locator('input[name="password"]').fill(credentials["password"])
    page.get_by_role("button", name="Log In").click()
    expect(page).to_have_url("https://parabank.parasoft.com/parabank/overview.htm")
