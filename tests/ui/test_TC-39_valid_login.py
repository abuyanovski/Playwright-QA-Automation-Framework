import re

from playwright.sync_api import expect


def test_TC39_valid_login(page):
    # Arrange
    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.get_by_role("link", name="Register").click()

    # Use regex to verify the URL contains the expected registration page path,
    # while allowing the domain or preceding URL path to vary
    expect(page).to_have_url(re.compile(r".*register\.htm"))

    page.locator('[name="customer.firstName"]').fill("Bill")
    page.locator('[name="customer.lastName"]').fill("Jones")
    page.locator('[name="customer.address.street"]').fill("1416 Orange Pekoe st")
    page.locator('[name="customer.address.city"]').fill("Los Angeles")
    page.locator('[name="customer.address.state"]').fill("Bill")
    page.locator('[name="customer.address.zipCode"]').fill("91324")
    page.locator('[name="customer.phoneNumber"]').fill("213-867-5309")
    page.locator('[name="customer.ssn"]').fill("123-45-6789")

    page.locator('[name="customer.username"]').fill("qa_user_20260914111342_583**1")
    page.locator('[name="customer.password"]').fill("ComplicatedPassword_1234")
    page.locator('[name="repeatedPassword"]').fill("ComplicatedPassword_1234")

    page.get_by_role("button", name="Register").click()

    # Act

    # Assert
