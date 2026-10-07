import json
import re
import uuid

from playwright.sync_api import Page, expect


# Terminal colors. RESET returns the text to its normal appearance.
BLUE = "\033[1;34m"
CYAN = "\033[36m"
DIM = "\033[2m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


def test_register_new_user(page: Page):
    """Register a customer, verify success and login, then save the credentials."""
    # Expected-result messages describe the scenario; expect() calls enforce checks.
    # Arrange: open the registration form before preparing fresh credentials.
    print(f"\n{BLUE}=================================================={RESET}")
    print(f"{BLUE}           ◆ TC-44: ACCOUNT CREATION{RESET}")
    print(f"{BLUE}=================================================={RESET}")

    print(f"\n{CYAN}› [1] Open the login page{RESET}")
    print(f"{DIM}    ↳ Expected: ParaBank login page is visible.{RESET}")
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    print(f"\n{CYAN}› [2] Click Register{RESET}")
    print(f"{DIM}    ↳ Expected: Customer Registration is displayed.{RESET}")
    page.get_by_role("link", name="Register").click()

    # Check the registration path without tying the assertion to the full site URL.
    expect(page).to_have_url(re.compile(r".*register\.htm"))

    # A fresh username avoids conflicts with accounts created by earlier runs.
    username = f"qa{uuid.uuid4().hex[:12]}"
    password = "Test1234"

    # Act: use fixed sample customer data so only the username changes between runs.
    print(f"\n{CYAN}› [3] Enter customer information{RESET}")
    print(f"{DIM}    ↳ Expected: Personal and address fields are filled.{RESET}")
    page.locator('[name="customer.firstName"]').fill("Anton")
    page.locator('[name="customer.lastName"]').fill("Tester")
    page.locator('[name="customer.address.street"]').fill("123 Test Street")
    page.locator('[name="customer.address.city"]').fill("Seattle")
    page.locator('[name="customer.address.state"]').fill("WA")
    page.locator('[name="customer.address.zipCode"]').fill("98101")
    page.locator('[name="customer.phoneNumber"]').fill("2065551234")
    page.locator('[name="customer.ssn"]').fill("123456789")

    print(f"\n{CYAN}› [4] Enter a unique username{RESET}")
    print(f"{DIM}    ↳ Expected: Username appears in the field.{RESET}")
    print(f"{DIM}    ↳ Username: {username}{RESET}")
    page.locator('[name="customer.username"]').fill(username)

    print(f"\n{CYAN}› [5] Enter the password{RESET}")
    print(f"{DIM}    ↳ Expected: Password is entered and masked.{RESET}")
    page.locator('[name="customer.password"]').fill(password)

    # Reuse the password variable so the confirmation matches the original entry.
    print(f"\n{CYAN}› [6] Confirm the password{RESET}")
    print(f"{DIM}    ↳ Expected: Both password fields match.{RESET}")
    page.locator('[name="repeatedPassword"]').fill(password)

    print(f"\n{CYAN}› [7] Submit registration{RESET}")
    print(f"{DIM}    ↳ Expected: Registration request is submitted.{RESET}")
    page.get_by_role("button", name="Register").click()

    print(f"\n{CYAN}› [8] Check the registration confirmation{RESET}")
    print(f"{DIM}    ↳ Expected: Account creation is confirmed.{RESET}")

    # Include the server response in captured test output to help diagnose failures.
    response_text = page.locator("#rightPanel").inner_text()
    print(f"{DIM}    ↳ Response:{RESET}")
    print(DIM + "      " + response_text.replace("\n", "\n      ") + RESET)

    # Wait for the success text before treating registration as successful.
    expect(page.locator("#rightPanel")).to_contain_text(
        "Your account was created successfully."
    )

    # Use Accounts Overview in the sidebar as the check for authenticated navigation.
    print(f"\n{CYAN}› [9] Check authentication{RESET}")
    print(f"{DIM}    ↳ Expected: Accounts Overview navigation is visible.{RESET}")
    expect(page.locator("#leftPanel")).to_contain_text(
        "Accounts Overview"
    )

    # Replace the credentials for future login tests only after both checks pass.
    with open("data/active_user.json", "w") as file:
        json.dump(
            {
                "username": username,
                "password": password
            },
            file,
            indent=4
        )

    print(f"\n{GREEN}--------------------------------------------------{RESET}")
    print(f"{GREEN}✓ PASS: Account created and credentials saved.{RESET}")
    print(f"{GREEN}--------------------------------------------------{RESET}")
    print(f"{DIM}    ↳ Username: {username}{RESET}")
    # The password is saved in the credentials file but kept out of console output.
    print(f"{DIM}    ↳ Password: [hidden]{RESET}")
