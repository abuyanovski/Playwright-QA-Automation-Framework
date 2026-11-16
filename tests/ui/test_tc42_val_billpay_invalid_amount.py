import json
import re
from decimal import Decimal
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect


# Terminal colors. RESET returns the text to its normal appearance.
BLUE = "\033[1;34m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

BASE_URL = "https://parabank.parasoft.com/parabank/"


def _read_account_state(page: Page, account_id: str) -> tuple[Decimal, set[int]]:
    """Read the balance and transaction IDs without leaving the payment form."""
    account_url = f"{BASE_URL}services_proxy/bank/accounts/{account_id}"
    account_response = page.request.get(account_url, headers={"Accept": "application/json"})
    assert account_response.ok, (
        f"Could not read account {account_id}: HTTP {account_response.status}."
    )
    transactions_response = page.request.get(
        f"{account_url}/transactions/month/All/type/All",
        headers={"Accept": "application/json"},
    )
    assert transactions_response.ok, (
        f"Could not read account {account_id} activity: HTTP {transactions_response.status}."
    )
    balance = Decimal(str(account_response.json()["balance"]))
    transaction_ids = {transaction["id"] for transaction in transactions_response.json()}
    return balance, transaction_ids


# Step 11 is automated: each variation gets a fresh page and its own pytest result.
@pytest.mark.parametrize(
    ("variation", "amount"),
    [
        pytest.param("empty", "", id="empty"),
        pytest.param("zero", "0.00", id="zero"),
        pytest.param("negative", "-25.00", id="negative"),
        pytest.param("nonnumeric", "abc", id="nonnumeric"),
    ],
)
def test_tc42_val_billpay_invalid_amount(page: Page, variation: str, amount: str) -> None:
    """Reject invalid bill payments without changing the source account.

    Requires valid saved credentials and an existing account. Run TC-44 if the
    saved credentials are rejected. Run sequentially without other account changes.
    """
    credentials_path = Path(__file__).resolve().parents[2] / "data" / "active_user.json"
    with credentials_path.open(encoding="utf-8") as file:
        credentials = json.load(file)

    print(f"\n{BLUE}=================================================={RESET}")
    print(f"{BLUE}       ◆ TC-42: BILL PAY INVALID PAYMENT AMOUNTS{RESET}")
    print(f"{BLUE}=================================================={RESET}")
    print(f"{DIM}    ↳ Automated variation: {variation}; amount: {amount!r}{RESET}")

    print(f"\n{CYAN}› [1] Log in with valid customer credentials{RESET}")
    print(f"{DIM}    ↳ Expected: Customer is authenticated successfully.{RESET}")
    page.goto(f"{BASE_URL}index.htm")
    expect(page.get_by_role("img", name="ParaBank")).to_be_visible()
    page.locator('input[name="username"]').fill(credentials["username"])
    page.locator('input[name="password"]').fill(credentials["password"])
    page.get_by_role("button", name="Log In", exact=True).click()
    expect(
        page.get_by_role("link", name="Log Out", exact=True),
        "TC-42 setup failed: valid saved credentials are required. "
        "If ParaBank rejects them, run TC-44 to register a fresh customer.",
    ).to_be_visible(timeout=10_000)
    expect(page.locator("#loginPanel")).to_be_hidden()

    print(f"\n{CYAN}› [2] Navigate to Bill Pay{RESET}")
    print(f"{DIM}    ↳ Expected: The Bill Pay page loads successfully.{RESET}")
    page.get_by_role("link", name="Bill Pay", exact=True).click()
    expect(page.get_by_role("heading", name="Bill Payment Service", exact=True)).to_be_visible()
    payment_form = page.locator("#billpayForm")
    expect(payment_form).to_be_visible()

    print(f"\n{CYAN}› [3] Enter valid payee name and address information{RESET}")
    print(f"{DIM}    ↳ Expected: Payee name, address, and required phone number are entered.{RESET}")
    payee_details = {
        "payee.name": f"TC42 Utilities {variation}",
        "payee.address.street": "123 Test Street",
        "payee.address.city": "Seattle",
        "payee.address.state": "WA",
        "payee.address.zipCode": "98101",
        "payee.phoneNumber": "2065551234",
    }
    for field_name, value in payee_details.items():
        field = payment_form.locator(f'input[name="{field_name}"]')
        field.fill(value)
        expect(field).to_have_value(value)

    print(f"\n{CYAN}› [4] Enter valid payee account information{RESET}")
    print(f"{DIM}    ↳ Expected: Both payee account fields contain the same numeric value.{RESET}")
    payee_account = "123456789"
    account_field = payment_form.locator('input[name="payee.accountNumber"]')
    verify_account_field = payment_form.locator('input[name="verifyAccount"]')
    account_field.fill(payee_account)
    verify_account_field.fill(payee_account)
    expect(account_field).to_have_value(payee_account)
    expect(verify_account_field).to_have_value(payee_account)

    print(f"\n{CYAN}› [5] Select a valid source account{RESET}")
    print(f"{DIM}    ↳ Expected: An existing source account is selected successfully.{RESET}")
    source_dropdown = payment_form.locator('select[name="fromAccountId"]')
    expect(source_dropdown.locator("option").first).to_have_text(re.compile(r"^\d+$"))
    source_account = source_dropdown.locator("option").first.inner_text().strip()
    source_dropdown.select_option(value=source_account)
    expect(source_dropdown).to_have_value(source_account)
    starting_balance, starting_transaction_ids = _read_account_state(page, source_account)
    print(f"{DIM}    ↳ Source {source_account}; starting balance: ${starting_balance:.2f}{RESET}")

    print(f"\n{CYAN}› [6] Enter the payment amount for this variation{RESET}")
    print(f"{DIM}    ↳ Expected: The amount field contains {amount!r}.{RESET}")
    amount_field = payment_form.locator('input[name="amount"]')
    amount_field.fill(amount)
    expect(amount_field).to_have_value(amount)

    print(f"\n{CYAN}› [7] Submit the bill payment{RESET}")
    print(f"{DIM}    ↳ Expected: The application validates the payment amount.{RESET}")
    payment_form.get_by_role("button", name="Send Payment", exact=True).click()
    # Wait for an actual outcome before checking that confirmation is absent.
    outcome = page.locator(
        "#validationModel-amount-empty:visible, "
        "#validationModel-amount-invalid:visible, "
        "#billpayResult:visible, #billpayError:visible"
    )
    expect(outcome, f"No payment or validation outcome appeared for {variation}.").to_have_count(
        1, timeout=35_000
    )

    print(f"\n{CYAN}› [8] Verify the invalid payment was not processed{RESET}")
    print(f"{DIM}    ↳ Expected: No success confirmation, balance change, or new transaction.{RESET}")
    ending_balance, ending_transaction_ids = _read_account_state(page, source_account)
    new_transaction_ids = ending_transaction_ids - starting_transaction_ids
    print(f"{DIM}    ↳ Balance: ${starting_balance:.2f} → ${ending_balance:.2f}{RESET}")
    print(f"{DIM}    ↳ New transaction IDs: {sorted(new_transaction_ids)}{RESET}")
    expect(
        page.locator("#billpayResult"),
        f"Invalid {variation} amount {amount!r} must not produce payment confirmation. "
        f"Balance: {starting_balance} -> {ending_balance}; "
        f"new transaction IDs: {sorted(new_transaction_ids)}.",
    ).to_be_hidden()
    assert ending_balance == starting_balance, (
        f"Invalid {variation} amount changed account {source_account}: "
        f"expected ${starting_balance:.2f}, found ${ending_balance:.2f}."
    )
    # A zero-dollar payment can create a transaction without changing the balance.
    assert ending_transaction_ids == starting_transaction_ids, (
        f"Invalid {variation} amount changed transaction history. "
        f"New IDs: {sorted(new_transaction_ids)}; "
        f"missing IDs: {sorted(starting_transaction_ids - ending_transaction_ids)}."
    )

    print(f"\n{CYAN}› [9] Verify an appropriate validation message{RESET}")
    print(f"{DIM}    ↳ Expected: Feedback identifies the amount as required or invalid.{RESET}")
    if variation == "empty":
        feedback = page.locator("#validationModel-amount-empty")
        expect(feedback).to_be_visible()
        expect(feedback).to_have_text("The amount cannot be empty.")
    elif variation == "nonnumeric":
        feedback = page.locator("#validationModel-amount-invalid")
        expect(feedback).to_be_visible()
        expect(feedback).to_have_text("Please enter a valid amount.")
    else:
        feedback = page.locator(
            "#validationModel-amount-invalid:visible, #billpayError .error:visible"
        )
        expect(feedback).to_be_visible()
        expect(feedback).to_contain_text(re.compile(r"\bamount\b", re.IGNORECASE))
        expect(feedback).to_contain_text(re.compile(
            r"\b(?:invalid|required|positive)\b|valid amount|greater than (?:zero|0)",
            re.IGNORECASE,
        ))

    print(f"\n{CYAN}› [10] Verify the customer can correct the input{RESET}")
    print(f"{DIM}    ↳ Expected: Bill Pay remains usable and the amount can be changed to 25.00.{RESET}")
    expect(page).to_have_url(re.compile(r"/billpay\.htm(?:[?#].*)?$"))
    expect(payment_form).to_be_visible()
    expect(amount_field).to_be_editable()
    amount_field.fill("25.00")
    expect(amount_field).to_have_value("25.00")
    # Check correction without sending a valid payment as part of this negative test.
    expect(payment_form.get_by_role("button", name="Send Payment", exact=True)).to_be_enabled()

    print(f"\n{GREEN}--------------------------------------------------{RESET}")
    print(f"{GREEN}✓ PASS: {variation} amount rejected; balance and history unchanged.{RESET}")
    print(f"{GREEN}--------------------------------------------------{RESET}")
