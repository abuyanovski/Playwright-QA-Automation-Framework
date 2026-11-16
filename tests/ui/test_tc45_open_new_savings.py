import json
import re
from pathlib import Path

from playwright.sync_api import Page, expect


# Terminal colors. RESET returns the text to its normal appearance.
BLUE = "\033[1;34m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


def test_tc45_open_new_savings(page: Page) -> None:
    """Open a savings account using saved credentials and verify its details."""
    credentials_path = Path(__file__).resolve().parents[2] / "data" / "active_user.json"
    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    print(f"\n{BLUE}=================================================={RESET}")
    print(f"{BLUE}          ◆ TC-45: OPEN NEW SAVINGS ACCOUNT{RESET}")
    print(f"{BLUE}=================================================={RESET}")

    print(f"\n{CYAN}› Setup: Log in with the saved credentials{RESET}")
    print(f"{DIM}    ↳ Expected: Account services and Log Out are visible.{RESET}")
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    expect(page.get_by_role("img", name="ParaBank")).to_be_visible()
    page.locator('input[name="username"]').fill(credentials["username"])
    page.locator('input[name="password"]').fill(credentials["password"])
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("link", name="Log Out", exact=True)).to_be_visible()
    expect(page.locator("#loginPanel")).to_be_hidden()

    print(f"\n{CYAN}› [1] Navigate to Accounts Overview{RESET}")
    print(f"{DIM}    ↳ Expected: An existing account number and balance are displayed.{RESET}")
    page.get_by_role("link", name="Accounts Overview", exact=True).click()
    expect(page.get_by_role("heading", name="Accounts Overview", exact=True)).to_be_visible()
    expect(page.locator("#accountTable")).to_be_visible()
    # Ignore the total row and wait for an account row to finish loading.
    existing_account_row = page.locator("#accountTable tbody tr").filter(
        has=page.locator("a")
    ).first
    existing_account_link = existing_account_row.get_by_role("link")
    expect(existing_account_link).to_have_text(re.compile(r"^\d+$"))
    existing_balance = existing_account_row.locator("td").nth(1)
    expect(existing_balance).to_be_visible()
    expect(existing_balance).to_have_text(re.compile(r"\$-?[\d,]+\.\d{2}"))

    print(f"\n{CYAN}› [2] Record the existing account number{RESET}")
    print(f"{DIM}    ↳ Expected: The original account number is available for comparison.{RESET}")
    original_account_number = existing_account_link.inner_text().strip()
    print(f"{DIM}    ↳ Original account: {original_account_number}{RESET}")

    print(f"\n{CYAN}› [3] Open New Account from the account services menu{RESET}")
    print(f"{DIM}    ↳ Expected: The Open New Account page is displayed.{RESET}")
    page.get_by_role("link", name="Open New Account", exact=True).click()
    expect(page.get_by_role("heading", name="Open New Account", exact=True)).to_be_visible()

    print(f"\n{CYAN}› [4] Select SAVINGS as the account type{RESET}")
    print(f"{DIM}    ↳ Expected: SAVINGS is selected as the new account type.{RESET}")
    account_type = page.locator("#type")
    account_type.select_option(label="SAVINGS")
    expect(account_type.locator("option:checked")).to_have_text("SAVINGS")

    print(f"\n{CYAN}› [5] Select the existing funding account{RESET}")
    print(f"{DIM}    ↳ Expected: The recorded account is selected as the funding source.{RESET}")
    funding_account = page.locator("#fromAccountId")
    # Account options load asynchronously; wait for the recorded account first.
    expect(funding_account.locator("option").filter(
        has_text=re.compile(rf"^{re.escape(original_account_number)}$")
    )).to_have_count(1)
    funding_account.select_option(label=original_account_number)
    expect(funding_account).to_have_value(original_account_number)

    print(f"\n{CYAN}› [6] Click Open New Account{RESET}")
    print(f"{DIM}    ↳ Expected: The account-opening request is submitted.{RESET}")
    page.get_by_role("button", name="Open New Account", exact=True).click()

    print(f"\n{CYAN}› [7] Verify the account creation confirmation{RESET}")
    print(f"{DIM}    ↳ Expected: A message confirms the new account was opened successfully.{RESET}")
    expect(page.get_by_role("heading", name="Account Opened!", exact=True)).to_be_visible()
    expect(page.locator("#rightPanel")).to_contain_text(
        "Congratulations, your account is now open."
    )

    print(f"\n{CYAN}› [8] Capture the new account number{RESET}")
    print(f"{DIM}    ↳ Expected: The new account number differs from the original.{RESET}")
    new_account_link = page.locator("#newAccountId")
    expect(new_account_link).to_be_visible()
    expect(new_account_link).to_have_text(re.compile(r"^\d+$"))
    new_account_number = new_account_link.inner_text().strip()
    assert new_account_number != original_account_number, (
        "The new savings account number must differ from the original account number."
    )
    print(f"{DIM}    ↳ New savings account: {new_account_number}{RESET}")

    print(f"\n{CYAN}› [9] Click the new account number{RESET}")
    print(f"{DIM}    ↳ Expected: The new account's details page is displayed.{RESET}")
    new_account_link.click()
    expect(page.get_by_role("heading", name="Account Details", exact=True)).to_be_visible()

    print(f"\n{CYAN}› [10] Verify the new account type and information{RESET}")
    print(f"{DIM}    ↳ Expected: The account number matches and the account type is SAVINGS.{RESET}")
    expect(page.locator("#accountId")).to_have_text(new_account_number)
    expect(page.locator("#accountType")).to_have_text("SAVINGS")

    print(f"\n{GREEN}--------------------------------------------------{RESET}")
    print(f"{GREEN}✓ PASS: New savings account opened and details verified.{RESET}")
    print(f"{GREEN}--------------------------------------------------{RESET}")
