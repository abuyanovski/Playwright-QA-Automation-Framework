import json
from pathlib import Path

from playwright.sync_api import Page, expect


# Terminal colors. RESET returns the text to its normal appearance.
BLUE = "\033[1;34m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


def test_tc39_valid_login(page: Page) -> None:
    """Log in with the saved credentials and verify account access."""
    credentials_path = Path(__file__).resolve().parents[2] / "data" / "active_user.json"
    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    print(f"\n{BLUE}=================================================={RESET}")
    print(f"{BLUE}              ◆ TC-39: VALID LOGIN{RESET}")
    print(f"{BLUE}=================================================={RESET}")

    print(f"\n{CYAN}› [1] Open the login page{RESET}")
    print(f"{DIM}    ↳ Expected: ParaBank login page is visible.{RESET}")
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    expect(page.get_by_role("img", name="ParaBank")).to_be_visible()

    print(f"\n{CYAN}› [2] Enter the saved username{RESET}")
    print(f"{DIM}    ↳ Expected: Username appears in the field.{RESET}")
    page.locator('input[name="username"]').fill(credentials["username"])

    print(f"\n{CYAN}› [3] Enter the saved password{RESET}")
    print(f"{DIM}    ↳ Expected: Password is entered and masked.{RESET}")
    page.locator('input[name="password"]').fill(credentials["password"])

    print(f"\n{CYAN}› [4] Click Log In{RESET}")
    print(f"{DIM}    ↳ Expected: Login request is submitted.{RESET}")
    page.get_by_role("button", name="Log In").click()

    print(f"\n{CYAN}› [5] Check authentication{RESET}")
    print(f"{DIM}    ↳ Expected: Account area and Log Out are visible.{RESET}")
    expect(page.get_by_role("link", name="Log Out", exact=True)).to_be_visible()
    expect(page.locator("#loginPanel")).to_be_hidden()

    print(f"\n{CYAN}› [6] Check for login errors{RESET}")
    print(f"{DIM}    ↳ Expected: No login error is displayed.{RESET}")
    expect(page.locator("#rightPanel .error")).to_be_hidden()

    print(f"\n{CYAN}› [7] Check Accounts Overview{RESET}")
    print(f"{DIM}    ↳ Expected: Customer accounts and balances are visible.{RESET}")
    expect(page).to_have_url("https://parabank.parasoft.com/parabank/overview.htm")
    expect(page.locator("#accountTable")).to_be_visible()

    # Manual reminder: this test currently uses one saved credential combination.
    print(f"\n{CYAN}↻ [8] Repeat with other valid accounts (manual){RESET}")
    print(f"{DIM}    ↳ Expected: Each valid account can log in.{RESET}")

    print(f"\n{GREEN}--------------------------------------------------{RESET}")
    print(f"{GREEN}✓ PASS: Login checks completed for the saved account.{RESET}")
    print(f"{GREEN}--------------------------------------------------{RESET}")
