# Playwright QA Automation Framework

A developing QA automation portfolio built with Python, Playwright, and pytest. The current focus is practicing browser automation against ParaBank while building reusable page objects, test fixtures, and QA documentation.

**Status: work in progress.** Registration and valid-login scenarios are implemented. Page objects, reusable fixtures, and placeholder directories support further development. Implemented coverage does not imply a verified passing run against the public demo site.

## Current Implementation

There are two active UI test functions across two files:

| File | Current behavior | Status |
| --- | --- | --- |
| [test_TC-44_new_ user_account_creation.py](tests/ui/test_TC-44_new_%20user_account_creation.py) | Registers a customer with a unique username, checks the success message and account-services sidebar, then saves credentials to `data/active_user.json`. | Uses pytest's `page` fixture and direct Playwright calls. |
| [test_TC-39_valid_login.py](tests/ui/test_TC-39_valid_login.py) | Reads the saved username and password, fills the login form, submits it, and checks that the URL is `https://parabank.parasoft.com/parabank/overview.htm`. | Uses pytest's `page` fixture; requires an existing valid account in the JSON file. |

Page objects for login, registration, account overview, opening accounts, transfers, and bill payments remain available in `pages/`. The two active tests currently use direct browser interactions.

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

Run these commands from the repository root. First register an account to populate `data/active_user.json`, then run the login test:

```powershell
# TC-44: create an account and save its credentials
.\.venv\Scripts\python.exe -m pytest "tests/ui/test_TC-44_new_ user_account_creation.py"

# TC-39: log in using the saved credentials
.\.venv\Scripts\python.exe -m pytest "tests/ui/test_TC-39_valid_login.py"

# Inspect discovery without executing browser workflows
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

The registration filename contains a space after `new_`, so keep the quotes around its path. Both files are pytest tests; use `-m pytest` to supply the `page` fixture and run their assertions.

To run both scenarios in one command with fresh credentials, specify registration before login and stop if registration fails:

```powershell
.\.venv\Scripts\python.exe -m pytest -x "tests/ui/test_TC-44_new_ user_account_creation.py" "tests/ui/test_TC-39_valid_login.py"
```

The login test does not automatically run registration. A plain `pytest` run discovers both files but does not establish this dependency; prepare valid saved credentials first or use the ordered command above.

Both active tests hardcode the public ParaBank URL, so they do not require `--base-url`. The reusable page objects accept a base URL for future tests.

The execution defaults are verbose output, short tracebacks, a visible Chromium browser, and a 500 ms action delay (`--headed --slowmo 500`).

```powershell
# Select Firefox after installing its browser binary
.\.venv\Scripts\python.exe -m pytest "tests/ui/test_TC-39_valid_login.py" --browser firefox

# Replace the demo defaults for headless execution without the action delay
.\.venv\Scripts\python.exe -m pytest "tests/ui/test_TC-39_valid_login.py" -o "addopts=-v --tb=short"
```

The configuration registers `ui`, `api`, `integration`, `smoke`, and `regression` markers. Neither active test currently has a marker, so filtering with these markers selects no tests. Select tests by file path instead.

## Architecture and Project Structure

```text
pages/                       Page objects and shared navigation/assertion helpers
tests/
    ui/
        conftest.py          Reusable customer and registered-customer fixtures
        test_TC-39_valid_login.py
        test_TC-44_new_ user_account_creation.py
    api/                     Placeholder
    integration/             Placeholder
data/
    active_user.json         Credentials saved by TC-44 and read by TC-39
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

The page objects group locators, browser actions, and UI checks for reuse. The current registration and login tests have not yet been migrated to those helpers.

The function-scoped `customer` fixture generates a customer with a timestamp and random username suffix. `registered_customer` registers that customer through the UI and checks registration success before returning it. These fixtures and the `sample_payee()` generator are available for future tests. The active tests use the `page` fixture from pytest-playwright, which manages browser setup and cleanup.

The unused generator and placeholder directories represent work that has not yet been connected to the active suite.

## Test Data and Saved Credentials

`data/active_user.json` contains the `username` (UID) and `password` fields. TC-44 replaces it after the registration-success and account-navigation assertions pass. TC-39 reads both values with `json.load()` and fills the login form with them.

The login test resolves the JSON path relative to its own file, so reading the credentials does not depend on the terminal's working directory. Registration writes to `data/active_user.json` relative to the working directory, so run registration from the repository root.

If the file is missing or the saved account no longer exists on the shared demo site, rerun TC-44 successfully before TC-39. Editing the JSON alone does not create an account on ParaBank.

Registration prints the username and displays `Password: [hidden]`; the password is stored in the JSON file. Although the JSON path is listed in `.gitignore`, the file is already tracked by Git, so updates can still appear in `git status`. Use synthetic demo credentials only.

## Reporting and QA Documentation

pytest provides console results. To generate a JUnit report and retain failure evidence:

```powershell
.\.venv\Scripts\python.exe -m pytest -x "tests/ui/test_TC-44_new_ user_account_creation.py" "tests/ui/test_TC-39_valid_login.py" --junitxml=reports/junit.xml --tracing retain-on-failure --screenshot only-on-failure
```

The XML report goes to `reports/junit.xml`; Playwright artifacts go to `test-results/`. These generated directories are ignored by Git. Traces and automatic screenshots are off unless enabled. No HTML dashboard, automated upload, or GitHub Actions workflow is configured.

- [Test strategy](docs/test-strategy.md): intended testing approach, including future test layers.
- [Test cases](docs/test-cases.md): current and proposed scenarios; the catalog is broader than implemented coverage.
- [Defect report example](docs/defect-report-example.md): an illustrative report format, not evidence of a currently reproduced defect. Its evidence filenames are examples.

Testiny is a future consideration mentioned in the intended workflow. It is not part of the current setup, and no integration or result upload is implemented.

## Current Limitations and Next Steps

- Add authenticated-page content checks to complement the login URL assertion.
- Remove the manual registration prerequisite by defining a reusable saved-account setup workflow.
- Add account-service tests using the existing page objects.
- Consolidate direct browser scripts, page objects, and data generation as the framework develops.
- Centralize the application URL and apply markers consistently.
- Improve synchronization and validate the current workflows before recording a passing baseline.
- Add negative cases and balance verification.
- Address saved-credential handling and test-data cleanup. Tests currently create server-side data without removing it.
- Add API, integration, and CI capabilities when their implementations are ready.

Tests depend on the availability and state of the external ParaBank demo instance. Failures need investigation before attributing them to either the framework or the application. Test discovery and the presence of assertions alone do not establish that a workflow passes.

See [LICENSE](LICENSE) for the repository's CC0 1.0 Universal terms.
