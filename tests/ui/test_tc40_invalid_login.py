import json
from pathlib import Path

from playwright.sync_api import Page, expect


# Terminal colors. RESET returns the text to its normal appearance.
BLUE = "\033[1;34m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


def test_tc40_invalid_login(page: Page) -> None:
    """Verify that incorrect credentials do not grant account access."""
    credentials_path = Path(__file__).resolve().parents[2] / "data" / "active_user.json"
    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    # Use incorrect variants of the saved credentials for this negative test.
    invalid_username = f"{credentials['username']}_invalid"
    invalid_password = f"{credentials['password']}_invalid"

    print(f"\n{BLUE}=================================================={RESET}")
    print(f"{BLUE}             ◆ TC-40: INVALID LOGIN{RESET}")
    print(f"{BLUE}=================================================={RESET}")

    print(f"\n{CYAN}› [1] Open the login page{RESET}")
    print(f"{DIM}    ↳ Expected: ParaBank login page is visible.{RESET}")
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    expect(page.get_by_role("img", name="ParaBank")).to_be_visible()

    print(f"\n{CYAN}› [2] Enter the incorrect username{RESET}")
    print(f"{DIM}    ↳ Expected: Username appears in the field.{RESET}")
    page.locator('input[name="username"]').fill(invalid_username)

    print(f"\n{CYAN}› [3] Enter the incorrect password{RESET}")
    print(f"{DIM}    ↳ Expected: Password is entered and masked.{RESET}")
    page.locator('input[name="password"]').fill(invalid_password)

    print(f"\n{CYAN}› [4] Click Log In{RESET}")
    print(f"{DIM}    ↳ Expected: Login request is submitted.{RESET}")
    page.get_by_role("button", name="Log In").click()

    print(f"\n{CYAN}› [5] Check that login is rejected{RESET}")
    print(f"{DIM}    ↳ Expected: User stays outside the account area.{RESET}")
    expect(page.locator("#loginPanel")).to_be_visible()

    print(f"\n{CYAN}› [6] Check the login error{RESET}")
    print(f"{DIM}    ↳ Expected: A login error is displayed.{RESET}")
    expect(page.locator("#rightPanel .error")).to_be_visible()

    print(f"\n{CYAN}› [7] Check that Accounts Overview is blocked{RESET}")
    print(f"{DIM}    ↳ Expected: No accounts or balances are visible.{RESET}")
    expect(page).not_to_have_url("https://parabank.parasoft.com/parabank/overview.htm")
    expect(page.locator("#accountTable")).to_be_hidden()

    # Manual reminder: this test currently uses one invalid credential combination.
    print(f"\n{CYAN}↻ [8] Repeat with other invalid credentials (manual){RESET}")
    print(f"{DIM}    ↳ Expected: Each invalid combination is rejected.{RESET}")

    print(f"\n{GREEN}--------------------------------------------------{RESET}")
    print(f"{GREEN}✓ PASS: Invalid-login checks completed.{RESET}")
    print(f"{GREEN}--------------------------------------------------{RESET}")
