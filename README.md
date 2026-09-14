# Playwright QA Automation Framework

A developing QA automation portfolio built with Python, Playwright, and pytest. The current focus is practicing browser automation against ParaBank while building reusable page objects, test fixtures, and QA documentation.

**Status: work in progress.** This README describes the code currently in the repository. Some scenarios are implemented, others are unfinished, and several directories are reserved for future work. The project does not currently claim a fully passing or complete test suite.

## Current Implementation

There are five active UI test functions across three files:

| File | Current behavior | Status |
| --- | --- | --- |
| [test_TC-39_account_creation.py](tests/ui/test_TC-39_account_creation.py) | Registers a customer with a unique username, checks the success message and account-services sidebar, then saves credentials to `data/active_user.json`. | Registration checks implemented using direct Playwright calls. |
| [test_TC39_valid_login.py](tests/ui/test_TC39_valid_login.py) | Opens registration and submits a form with a fixed username. | Unfinished: the login action and outcome assertions still need to be written. |
| [test_account_services.py](tests/ui/test_account_services.py) | Contains three scenarios: opening a savings account, transferring funds, and paying a bill. | Uses page objects and fresh-customer fixtures; marked `regression`. |

The savings-account test checks for a new account ID. The transfer test checks the confirmation amount and source/destination IDs. The bill-payment test checks the confirmation payee and amount. These checks do not yet verify resulting balances.

Login and logout helpers exist in `HomePage`, but the active login-named test does not currently use them. A passing result from that unfinished test would not prove that login works.

## Technology and Setup

The local project environment uses Python 3.14. [requirements.txt](requirements.txt) currently pins:

| Package | Version | Purpose |
| --- | --- | --- |
| pytest | 9.1.1 | Test discovery, execution, fixtures, and markers. |
| pytest-playwright | 0.9.0 | Browser/page fixtures and execution options. |
| Playwright | 1.62.0 | Browser automation and web assertions. |
| requests | 2.31.0 | Included for future API work; no project API client is implemented. |
| python-dotenv | 1.0.0 | Included for future configuration work; project code does not currently load a `.env` file. |

From the repository root in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install
```

Check that `python --version` selects the intended Python installation before creating the environment. Browser binaries are installed separately from the Python packages.

In PyCharm, select the project's `.venv\Scripts\python.exe` as the interpreter and the repository root as the working directory. A system interpreter may not have the project's dependencies. The commands below use the virtual environment directly, so activation is optional.

## Running the Current Tests

The page-object tests require a base URL. [pytest.ini](pytest.ini) does not currently provide one, so include the ParaBank application path when running the suite:

```powershell
# All current tests, including the unfinished login-named test
.\.venv\Scripts\python.exe -m pytest --base-url https://parabank.parasoft.com/parabank/

# The three account-service scenarios
.\.venv\Scripts\python.exe -m pytest -m regression --base-url https://parabank.parasoft.com/parabank/

# Standalone registration; successful execution replaces active_user.json
.\.venv\Scripts\python.exe -m pytest "tests/ui/test_TC-39_account_creation.py"

# Inspect discovery without executing browser workflows
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

Both TC39-related scripts hardcode the public ParaBank URL. Changing `--base-url` currently affects only the page-object flows.

The execution defaults are verbose output, short tracebacks, a visible Chromium browser, and a 500 ms action delay (`--headed --slowmo 500`).

```powershell
# Select Firefox after installing its browser binary
.\.venv\Scripts\python.exe -m pytest --browser firefox --base-url https://parabank.parasoft.com/parabank/

# Replace the demo defaults for headless execution without the action delay
.\.venv\Scripts\python.exe -m pytest -o "addopts=-v --tb=short" --base-url https://parabank.parasoft.com/parabank/
```

The configuration registers `ui`, `api`, `integration`, `smoke`, and `regression` markers. Only `regression` is currently applied to active tests. Consequently, `-m smoke` and `-m ui` select no tests; select `tests/ui` by path to run the UI directory.

## Architecture and Project Structure

```text
pages/                       Page objects and shared navigation/assertion helpers
tests/
    ui/
        conftest.py          Customer and registered-customer fixtures
        test_TC-39_account_creation.py
        test_TC39_valid_login.py
        test_account_services.py
    api/                     Placeholder
    integration/             Placeholder
data/
    active_user.json         Saved demo credentials from standalone registration
    user_data.py             Separate generator, not currently used by tests
utils/test_data.py           Customer/Payee models and synthetic data generators
api/                         Placeholder for future API clients
fixtures/                    Placeholder for future shared assets
conftest.py                  Placeholder for future shared fixtures
docs/                        Test strategy, case catalog, and example defect report
.github/workflows/           .gitkeep only; no CI workflow
pytest.ini                   Test discovery, markers, and browser defaults
requirements.txt             Pinned dependencies
LICENSE                      CC0 1.0 Universal
```

The account-service tests use the Page Object Model: tests express workflows, while page classes contain locators, browser actions, and UI checks. The two TC39-related scripts still contain direct browser interactions.

The function-scoped `customer` fixture generates a customer with a timestamp and random username suffix. `registered_customer` registers that customer through the UI and checks registration success before returning it. Bill-payment data comes from `sample_payee()`. Browser and page fixtures come from pytest-playwright.

The unused generator and placeholder directories represent work that has not yet been connected to the active suite.

## Test Data and Saved Credentials

`data/active_user.json` contains `username` and `password`. The standalone registration test replaces it after successful assertions. It is intended for future reuse, but **no active test currently reads it**, including the login-named test.

Account-service tests create their own customers through fixtures. They do not depend on the saved JSON account, and a saved record does not guarantee that an account still exists on the shared demo site.

The registration script currently stores demo credentials in plaintext and prints them in its output. Use synthetic test data. Although the JSON path is listed in `.gitignore`, the file is already tracked by Git; the ignore entry does not stop changes to that tracked file from being committed.

## Reporting and QA Documentation

pytest provides console results. To generate a JUnit report and retain failure evidence:

```powershell
.\.venv\Scripts\python.exe -m pytest --base-url https://parabank.parasoft.com/parabank/ --junitxml=reports/junit.xml --tracing retain-on-failure --screenshot only-on-failure
```

The XML report goes to `reports/junit.xml`; Playwright artifacts go to `test-results/`. These generated directories are ignored by Git. Traces and automatic screenshots are off unless enabled. No HTML dashboard, automated upload, or GitHub Actions workflow is configured.

- [Test strategy](docs/test-strategy.md): intended testing approach, including future test layers.
- [Test cases](docs/test-cases.md): current and proposed scenarios; the catalog is broader than implemented coverage.
- [Defect report example](docs/defect-report-example.md): an illustrative report format, not evidence of a currently reproduced defect. Its evidence filenames are examples.

Testiny is a future consideration mentioned in the intended workflow. It is not part of the current setup, and no integration or result upload is implemented.

## Current Limitations and Next Steps

- Complete the login scenario and its assertions; the fixed registration username can collide on repeat runs.
- Consolidate direct browser scripts, page objects, and data generation as the framework develops.
- Centralize the application URL and apply markers consistently.
- Improve synchronization and validate the current workflows before recording a passing baseline.
- Add negative cases and balance verification.
- Address saved-credential handling and test-data cleanup. Tests currently create server-side data without removing it.
- Add API, integration, and CI capabilities when their implementations are ready.

Tests depend on the availability and state of the external ParaBank demo instance. Failures need investigation before attributing them to either the framework or the application. Test discovery and the presence of assertions alone do not establish that a workflow passes.

See [LICENSE](LICENSE) for the repository's CC0 1.0 Universal terms.
