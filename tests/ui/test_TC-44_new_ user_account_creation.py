import json
import re
import uuid

from playwright.sync_api import Page, expect


def test_register_new_user(page: Page):
    """Register a customer, verify success and login, then save the credentials."""
    # Expected-result messages describe the scenario; expect() calls enforce checks.
    # Arrange: open the registration form before preparing fresh credentials.
    print("\nStep 1: Navigate to the ParaBank login page.")
    print("Expected result: ParaBank login page loads successfully.")
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    print("\nStep 2: Click Register.")
    print("Expected result: Customer Registration page is displayed.")
    page.get_by_role("link", name="Register").click()

    # Check the registration path without tying the assertion to the full site URL.
    expect(page).to_have_url(re.compile(r".*register\.htm"))

    # A fresh username avoids conflicts with accounts created by earlier runs.
    username = f"qa{uuid.uuid4().hex[:12]}"
    password = "Test1234"

    # Act: use fixed sample customer data so only the username changes between runs.
    print("\nStep 3: Enter valid customer information in the required personal and address fields.")
    print("Expected result: Customer information is accepted in the corresponding fields.")
    page.locator('[name="customer.firstName"]').fill("Anton")
    page.locator('[name="customer.lastName"]').fill("Tester")
    page.locator('[name="customer.address.street"]').fill("123 Test Street")
    page.locator('[name="customer.address.city"]').fill("Seattle")
    page.locator('[name="customer.address.state"]').fill("WA")
    page.locator('[name="customer.address.zipCode"]').fill("98101")
    page.locator('[name="customer.phoneNumber"]').fill("2065551234")
    page.locator('[name="customer.ssn"]').fill("123456789")

    print(f"\nStep 4: Enter a unique username in the Username field: {username}")
    print("Expected result: Username is accepted in the field.")
    page.locator('[name="customer.username"]').fill(username)

    print("\nStep 5: Enter a valid password in the Password field.")
    print("Expected result: Password is accepted and masked.")
    page.locator('[name="customer.password"]').fill(password)

    # Reuse the password variable so the confirmation matches the original entry.
    print("\nStep 6: Enter the same password in the Confirm Password field.")
    print("Expected result: Password confirmation is accepted and masked.")
    page.locator('[name="repeatedPassword"]').fill(password)

    print("\nStep 7: Click Register to submit the registration.")
    print("Expected result: Registration is submitted successfully.")
    page.get_by_role("button", name="Register").click()

    print("\nStep 8: Verify the registration success message is displayed.")
    print(
        "Expected result: A welcome message and confirmation that the account "
        "was created successfully are displayed."
    )

    # Include the server response in captured test output to help diagnose failures.
    response_text = page.locator("#rightPanel").inner_text()
    print(response_text)

    # Wait for the success text before treating registration as successful.
    expect(page.locator("#rightPanel")).to_contain_text(
        "Your account was created successfully."
    )

    # Use Accounts Overview in the sidebar as the check for authenticated navigation.
    print("\nStep 9: Verify the newly registered customer is logged in.")
    print(
        "Expected result: Authenticated customer navigation, account services, "
        "and logout options are displayed."
    )
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

    print("\nSuccessfully created and saved account")
    print(f"Username: {username}")
    # The password is saved in the credentials file but kept out of console output.
    print("Password: [hidden]")
