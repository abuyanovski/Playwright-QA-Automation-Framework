import re
import uuid

from playwright.sync_api import Page, expect


def test_register_new_user(page: Page):
    # Arrange
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    page.get_by_role("link", name="Register").click()

    # Use regex so the assertion focuses on the expected registration page path
    expect(page).to_have_url(re.compile(r".*register\.htm"))

    # Generate a unique username for each test run
    username = f"qa{uuid.uuid4().hex[:12]}"
    password = "Test1234"

    print(f"\nUsername being used: {username}")

    # Act
    page.locator('[name="customer.firstName"]').fill("Anton")
    page.locator('[name="customer.lastName"]').fill("Tester")
    page.locator('[name="customer.address.street"]').fill("123 Test Street")
    page.locator('[name="customer.address.city"]').fill("Seattle")
    page.locator('[name="customer.address.state"]').fill("WA")
    page.locator('[name="customer.address.zipCode"]').fill("98101")
    page.locator('[name="customer.phoneNumber"]').fill("2065551234")
    page.locator('[name="customer.ssn"]').fill("123456789")
    page.locator('[name="customer.username"]').fill(username)
    page.locator('[name="customer.password"]').fill(password)
    page.locator('[name="repeatedPassword"]').fill(password)

    page.get_by_role("button", name="Register").click()

    # Print ParaBank's response
    response_text = page.locator("#rightPanel").inner_text()
    print(response_text)

    # Assert
    expect(page.locator("#rightPanel")).to_contain_text(
        "Your account was created successfully."
    )

    expect(page.locator("#leftPanel")).to_contain_text("Accounts Overview")

    print(f"\nSuccessfully created account: {username}")
    print(username)