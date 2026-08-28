from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.test_data import Customer


class RegistrationPage(BasePage):
    def load(self) -> None:
        self.goto_path("register.htm")
        self.expect_heading("Signing up is easy!")

    def register(self, customer: Customer) -> None:
        self.page.locator("input[name='customer.firstName']").fill(customer.first_name)
        self.page.locator("input[name='customer.lastName']").fill(customer.last_name)
        self.page.locator("input[name='customer.address.street']").fill(customer.street)
        self.page.locator("input[name='customer.address.city']").fill(customer.city)
        self.page.locator("input[name='customer.address.state']").fill(customer.state)
        self.page.locator("input[name='customer.address.zipCode']").fill(customer.zip_code)
        self.page.locator("input[name='customer.phoneNumber']").fill(customer.phone)
        self.page.locator("input[name='customer.ssn']").fill(customer.ssn)
        self.page.locator("input[name='customer.username']").fill(customer.username)
        self.page.locator("input[name='customer.password']").fill(customer.password)
        self.page.locator("input[name='repeatedPassword']").fill(customer.password)
        self.page.locator("input[value='Register']").click()

    def expect_account_created(self, customer: Customer) -> None:
        self.expect_heading(f"Welcome {customer.username}")
        expect(self.page.locator("#rightPanel")).to_contain_text(
            "Your account was created successfully"
        )
