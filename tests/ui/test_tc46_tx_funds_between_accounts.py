import json
import re
from decimal import Decimal
from pathlib import Path

from playwright.sync_api import Page, expect


# Terminal colors. RESET returns the text to its normal appearance.
BLUE = "\033[1;34m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


def test_tc46_tx_funds_between_accounts(page: Page) -> None:
    """Transfer $25 between two existing accounts and verify balances and activity.

    Requires valid saved credentials and at least two accounts. The first account
    must have at least $25 available. Run TC-44 and TC-45 to prepare fresh accounts.
    """
    credentials_path = Path(__file__).resolve().parents[2] / "data" / "active_user.json"
    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    transfer_amount = Decimal("25.00")
    amount_text = f"{transfer_amount:.2f}"
    currency_pattern = re.compile(r"^-?\$[\d,]+\.\d{2}$")

    print(f"\n{BLUE}=================================================={RESET}")
    print(f"{BLUE}        ◆ TC-46: TRANSFER FUNDS BETWEEN ACCOUNTS{RESET}")
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
    print(f"{DIM}    ↳ Expected: Both the source and destination accounts are displayed.{RESET}")
    page.get_by_role("link", name="Accounts Overview", exact=True).click()
    expect(page.get_by_role("heading", name="Accounts Overview", exact=True)).to_be_visible()
    account_rows = page.locator("#accountTable tbody tr").filter(has=page.locator("a"))
    # Exclude the total row and wait for two account numbers to load.
    expect(account_rows.nth(0).get_by_role("link")).to_have_text(re.compile(r"^\d+$"))
    expect(
        account_rows.nth(1).get_by_role("link"),
        "TC-46 requires two accounts. Run TC-45 to open a second account.",
    ).to_have_text(re.compile(r"^\d+$"))
    source_account = account_rows.nth(0).get_by_role("link").inner_text().strip()
    destination_account = account_rows.nth(1).get_by_role("link").inner_text().strip()
    assert source_account != destination_account, "The transfer requires two different accounts."

    # Match by account number so later checks do not depend on table ordering.
    source_row = account_rows.filter(
        has=page.get_by_role("link", name=source_account, exact=True)
    )
    destination_row = account_rows.filter(
        has=page.get_by_role("link", name=destination_account, exact=True)
    )
    source_balance_cell = source_row.locator("td").nth(1)
    destination_balance_cell = destination_row.locator("td").nth(1)

    print(f"\n{CYAN}› [2] Record the current balances of both accounts{RESET}")
    print(f"{DIM}    ↳ Expected: Starting balances are available for comparison.{RESET}")
    expect(source_balance_cell).to_have_text(currency_pattern)
    expect(destination_balance_cell).to_have_text(currency_pattern)
    # Decimal keeps money calculations exact, including cents and comma separators.
    source_starting_balance = Decimal(
        source_balance_cell.inner_text().strip().replace("$", "").replace(",", "")
    )
    destination_starting_balance = Decimal(
        destination_balance_cell.inner_text().strip().replace("$", "").replace(",", "")
    )
    source_available_cell = source_row.locator("td").nth(2)
    expect(source_available_cell).to_have_text(currency_pattern)
    source_available = Decimal(
        source_available_cell.inner_text().strip().replace("$", "").replace(",", "")
    )
    assert source_available >= transfer_amount, (
        f"Source account {source_account} needs at least ${amount_text} available; "
        f"only ${source_available:.2f} is available."
    )
    print(f"{DIM}    ↳ Source {source_account}: ${source_starting_balance:.2f}{RESET}")
    print(f"{DIM}    ↳ Destination {destination_account}: ${destination_starting_balance:.2f}{RESET}")

    # Save existing transaction links so an older $25 transfer cannot satisfy step 12.
    print(f"{DIM}    ↳ Record the source account's existing transactions for comparison.{RESET}")
    with page.expect_response(re.compile(
        rf"/accounts/{source_account}/transactions/month/All/type/All$"
    )) as activity_response:
        source_row.get_by_role("link", name=source_account, exact=True).click()
    response = activity_response.value
    assert response.ok, f"Source account activity failed to load: HTTP {response.status}."
    expect(page.locator("#accountId")).to_have_text(source_account)
    transaction_rows = page.locator("#transactionTable tbody tr")
    # The response count lets us wait for all rows, including an empty history.
    expect(transaction_rows).to_have_count(len(response.json()))
    existing_transaction_links = {
        link.get_attribute("href")
        for link in transaction_rows.get_by_role("link").all()
    }

    print(f"\n{CYAN}› [3] Click Transfer Funds from the account services menu{RESET}")
    print(f"{DIM}    ↳ Expected: The Transfer Funds page is displayed.{RESET}")
    page.get_by_role("link", name="Transfer Funds", exact=True).click()
    expect(page.get_by_role("heading", name="Transfer Funds", exact=True)).to_be_visible()

    print(f"\n{CYAN}› [4] Enter a valid transfer amount{RESET}")
    print(f"{DIM}    ↳ Expected: ${amount_text} is entered successfully.{RESET}")
    page.locator("#amount").fill(amount_text)
    expect(page.locator("#amount")).to_have_value(amount_text)

    print(f"\n{CYAN}› [5] Select the source account in the From dropdown{RESET}")
    print(f"{DIM}    ↳ Expected: Source account {source_account} is selected.{RESET}")
    from_account = page.locator("#fromAccountId")
    expect(from_account.locator(f'option[value="{source_account}"]')).to_have_count(1)
    from_account.select_option(value=source_account)
    expect(from_account).to_have_value(source_account)

    print(f"\n{CYAN}› [6] Select the destination account in the To dropdown{RESET}")
    print(f"{DIM}    ↳ Expected: Destination account {destination_account} is selected.{RESET}")
    to_account = page.locator("#toAccountId")
    expect(to_account.locator(f'option[value="{destination_account}"]')).to_have_count(1)
    to_account.select_option(value=destination_account)
    expect(to_account).to_have_value(destination_account)

    print(f"\n{CYAN}› [7] Click Transfer{RESET}")
    print(f"{DIM}    ↳ Expected: The transfer request is submitted.{RESET}")
    page.get_by_role("button", name="Transfer", exact=True).click()

    print(f"\n{CYAN}› [8] Verify the transfer confirmation{RESET}")
    print(f"{DIM}    ↳ Expected: Success confirms the amount and both account numbers.{RESET}")
    expect(page.get_by_role("heading", name="Transfer Complete!", exact=True)).to_be_visible()
    expect(page.locator("#amountResult")).to_have_text(f"${amount_text}")
    expect(page.locator("#fromAccountIdResult")).to_have_text(source_account)
    expect(page.locator("#toAccountIdResult")).to_have_text(destination_account)
    expect(page.locator("#showError")).to_be_hidden()

    print(f"\n{CYAN}› [9] Return to Accounts Overview{RESET}")
    print(f"{DIM}    ↳ Expected: Both accounts are displayed with updated balances.{RESET}")
    page.get_by_role("link", name="Accounts Overview", exact=True).click()
    expect(page.get_by_role("heading", name="Accounts Overview", exact=True)).to_be_visible()
    expect(source_row).to_be_visible()
    expect(destination_row).to_be_visible()
    expect(source_balance_cell).to_have_text(currency_pattern)
    expect(destination_balance_cell).to_have_text(currency_pattern)

    print(f"\n{CYAN}› [10] Verify the source-account balance{RESET}")
    print(f"{DIM}    ↳ Expected: The source balance decreased by exactly ${amount_text}.{RESET}")
    source_ending_balance = Decimal(
        source_balance_cell.inner_text().strip().replace("$", "").replace(",", "")
    )
    expected_source_balance = source_starting_balance - transfer_amount
    assert source_ending_balance == expected_source_balance, (
        f"Source account {source_account}: expected ${expected_source_balance:.2f}, "
        f"but found ${source_ending_balance:.2f}."
    )
    print(f"{DIM}    ↳ Source {source_account}: ${source_ending_balance:.2f}{RESET}")

    print(f"\n{CYAN}› [11] Verify the destination-account balance{RESET}")
    print(f"{DIM}    ↳ Expected: The destination balance increased by exactly ${amount_text}.{RESET}")
    destination_ending_balance = Decimal(
        destination_balance_cell.inner_text().strip().replace("$", "").replace(",", "")
    )
    expected_destination_balance = destination_starting_balance + transfer_amount
    assert destination_ending_balance == expected_destination_balance, (
        f"Destination account {destination_account}: expected ${expected_destination_balance:.2f}, "
        f"but found ${destination_ending_balance:.2f}."
    )
    print(f"{DIM}    ↳ Destination {destination_account}: ${destination_ending_balance:.2f}{RESET}")

    print(f"\n{CYAN}› [12] Open the source account activity{RESET}")
    print(f"{DIM}    ↳ Expected: A new transfer debit for ${amount_text} is visible.{RESET}")
    source_row.get_by_role("link", name=source_account, exact=True).click()
    expect(page.get_by_role("heading", name="Account Activity", exact=True)).to_be_visible()
    expect(page.locator("#accountId")).to_have_text(source_account)
    expect(transaction_rows).to_have_count(len(existing_transaction_links) + 1)
    new_transaction_links = [
        link for link in transaction_rows.get_by_role("link").all()
        if link.get_attribute("href") not in existing_transaction_links
    ]
    assert len(new_transaction_links) == 1, "Expected exactly one new source transaction."
    new_transaction_link = new_transaction_links[0]
    expect(new_transaction_link).to_have_text("Funds Transfer Sent")
    expect(new_transaction_link).to_be_visible()
    new_transaction_href = new_transaction_link.get_attribute("href")
    new_transaction_row = transaction_rows.filter(
        has=page.locator(f'a[href="{new_transaction_href}"]')
    )
    expect(new_transaction_row.locator("td").nth(2)).to_have_text(f"${amount_text}")
    expect(new_transaction_row.locator("td").nth(3)).to_be_empty()

    print(f"\n{GREEN}--------------------------------------------------{RESET}")
    print(f"{GREEN}✓ PASS: Transfer confirmation, balances, and new source debit verified.{RESET}")
    print(f"{GREEN}--------------------------------------------------{RESET}")
