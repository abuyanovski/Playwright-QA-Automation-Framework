# Playwright QA Automation Framework

A QA automation portfolio built with Python, Playwright, and pytest against the public ParaBank demo. Coverage includes registration, login, invalid bill-payment amounts, savings-account creation, and transfers.

**Status: work in progress.** Six UI test functions produce nine pytest cases. The November 16, 2026 local Chromium run finished with **7 passed, 2 failed**. Both failures expose invalid bill payments being processed by ParaBank; see [verification results](#verification-results). GitHub Actions runs registration before the remaining scenarios.

## Current Tests

| Test case | File | What it checks |
| --- | --- | --- |
| TC-44: Account creation | [test_tc44_new_user_account_creation.py](tests/ui/test_tc44_new_user_account_creation.py) | Registers a unique customer, checks registration confirmation and account navigation, then saves credentials. |
| TC-39: Valid login | [test_tc39_valid_login.py](tests/ui/test_tc39_valid_login.py) | Reads saved credentials and checks authenticated navigation, no visible login error, the Accounts Overview URL, and the account table. |
| TC-40: Invalid login | [test_tc40_invalid_login.py](tests/ui/test_tc40_invalid_login.py) | Adds `_invalid` to the saved username and password, submits them, and checks that login is rejected, an error is visible, and account information is hidden. |
| TC-42: Invalid bill-payment amounts | [test_tc42_val_billpay_invalid_amount.py](tests/ui/test_tc42_val_billpay_invalid_amount.py) | Automates empty, zero, negative, and nonnumeric amounts; checks rejection, feedback, unchanged balance and transaction history, and editable input. |
| TC-45: Open savings account | [test_tc45_open_new_savings.py](tests/ui/test_tc45_open_new_savings.py) | Opens a savings account using an existing funding account and checks confirmation, a different account number, and SAVINGS account details. |
| TC-46: Transfer funds | [test_tc46_tx_funds_between_accounts.py](tests/ui/test_tc46_tx_funds_between_accounts.py) | Transfers $25, checks confirmation and exact changes to both balances, and verifies one new source-account debit. |

Each login test currently uses one credential combination. Its printed Step 8 is a manual repeat reminder; additional login variations and missing-field cases are not automated yet. TC-42's four amount variations are automated and receive separate pytest results.

TC-42 uses authenticated API reads to compare balances and transaction IDs without leaving the payment form. A zero-dollar payment can create a transaction without changing the balance. TC-46 uses Decimal for money calculations and compares transaction links so an older transfer cannot satisfy its final assertion. These checks support the UI scenarios; standalone API and integration suites remain planned.

## Verification Results

On November 16, 2026, discovery collected nine cases. A headless Chromium run using the repository virtual environment (Python 3.14.10, pytest 9.1.1) produced **7 passed, 2 failed** across registration and the dependent tests:

- **Passed:** TC-44, TC-39, TC-45, TC-46, TC-40, and the empty/nonnumeric TC-42 cases.
- **TC-42 zero amount failed:** ParaBank displayed a success confirmation for `0.00` and created a transaction while the balance stayed at $390.50.
- **TC-42 negative amount failed:** ParaBank displayed a success confirmation for `-25.00`, created a transaction, and increased the selected account balance from $125.00 to $150.00.

Both failures occurred at the assertion requiring payment confirmation to be hidden. The tests recorded the balance and transaction changes before asserting, so the diagnostics also show the account effects. Rejection assertions remain strict; the failures are not skipped or marked as expected passes.

See the [dated validation record](docs/validation-2026-11-16.md) for commands, per-case results, and evidence locations. These observations describe that run of a shared demo, not a guarantee of its future state.

### Known ParaBank Defect

**Historical login observation:** TC-40 failed in the October run below and passed in the November 16 local run. The newer pass does not establish that every invalid-login combination is fixed.

In the [October 7, 2026 CI run](https://github.com/abuyanovski/Playwright-QA-Automation-Framework/actions/runs/37704360018), TC-44 registration and TC-39 valid login passed. TC-40 invalid login failed, giving a result of **2 passed, 1 failed**.

- **Expected:** Incorrect credentials are rejected, a login error appears, and account information stays hidden.
- **Actual:** After submitting a username and password with `_invalid` appended, the page displayed “Welcome Anton Tester,” Accounts Overview, Log Out, and account balances.
- **Failure:** The assertion in [TC-40](tests/ui/test_tc40_invalid_login.py) expected `#loginPanel` to be visible, but the element was missing.

That workflow completed setup and ran the three tests available at the time. Its failed status reported the observed application behavior. TC-40 continues to enforce rejection of the incorrect credential combination.

## Project Structure and Cleanup

Unused page objects, customer/payee fixtures, and separate data generators have been removed. Test filenames now use consistent underscores without spaces or hyphens. Dependencies are limited to those used by the active tests.

Directories reserved for future work contain only `.gitkeep` placeholders. Their names describe planned areas, not implemented capabilities.

```text
.github/
    workflows/
        playwright-tests.yml           GitHub Actions UI test workflow
api/.gitkeep                            Future API clients
data/
    active_user.json                    Saved demo credentials
docs/
    README.md                          Documentation index
    test-cases.md                      Current and planned coverage
    test-strategy.md                    Current approach and future scope
    validation-2026-11-16.md            Recorded local execution and defects
    defect-report-example.md            Illustrative report template
fixtures/.gitkeep                       Future reusable test data/fixtures
pages/.gitkeep                          Future page objects
tests/
    ui/
        AGENTS.md                      Preferred console output style
        test_tc39_valid_login.py
        test_tc40_invalid_login.py
        test_tc42_val_billpay_invalid_amount.py
        test_tc44_new_user_account_creation.py
        test_tc45_open_new_savings.py
        test_tc46_tx_funds_between_accounts.py
    api/.gitkeep                        Future API tests
    integration/.gitkeep                Future integration tests
utils/.gitkeep                          Future shared helpers
AGENTS.md                               Project writing guidelines
conftest.py                             Placeholder for shared pytest fixtures
pytest.ini                              Discovery, markers, browser defaults
requirements.txt                        Active dependency pins
LICENSE                                 CC0 1.0 Universal
```

The active tests use direct Playwright calls. Browser setup and cleanup come from pytest-playwright's `page` fixture. Custom page objects and shared fixtures can be added when an implemented test needs them.

## Setup

[requirements.txt](requirements.txt) pins:

| Package | Version | Purpose |
| --- | --- | --- |
| pytest | 9.1.1 | Test discovery, execution, and results. |
| pytest-playwright | 0.9.0 | Browser/page fixtures and execution options. |
| playwright | 1.62.0 | Browser actions and web assertions. |

From the repository root in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

Choose the intended Python installation before creating the virtual environment. In PyCharm, select `.venv\Scripts\python.exe` as the interpreter and the repository root as the working directory.

## Running the Tests

Run registration successfully from the repository root before the remaining tests to create fresh `data/active_user.json` credentials:

```powershell
# TC-44: register and save credentials, headlessly
.\.venv\Scripts\python.exe -m pytest -s `
    tests/ui/test_tc44_new_user_account_creation.py `
    -o "addopts=-v --tb=short"

if ($LASTEXITCODE -ne 0) { throw "Registration failed; resolve setup before continuing." }

# Eight dependent cases, including all four TC-42 variations
.\.venv\Scripts\python.exe -m pytest -s `
    tests/ui/test_tc39_valid_login.py `
    tests/ui/test_tc45_open_new_savings.py `
    tests/ui/test_tc46_tx_funds_between_accounts.py `
    tests/ui/test_tc42_val_billpay_invalid_amount.py `
    tests/ui/test_tc40_invalid_login.py `
    -o "addopts=-v --tb=short"
```

TC-45 prepares the second account for TC-46. The first account must have at least $25 available. Run sequentially without other changes to the same accounts. The account-changing positive scenarios run before TC-42; pytest may group TC-42's parameterized cases around other independent tests.

After preparing valid credentials, run TC-42 on its own with:

```powershell
.\.venv\Scripts\python.exe -m pytest -s `
    tests/ui/test_tc42_val_billpay_invalid_amount.py `
    -o "addopts=-v --tb=short"
```

A plain `pytest` run discovers nine cases but does not establish registration or account-creation prerequisites. Use the ordered commands above for full verification. They do not stop at the first dependent-test failure.

To inspect discovery without opening browsers:

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

If an existing PyCharm run configuration points to an old filename, recreate it using the Run icon beside the test in its renamed file.

[pytest.ini](pytest.ini) defaults to verbose output, short tracebacks, a visible browser, and a 500 ms action delay (`--headed --slowmo 500`). All six test functions use the public ParaBank URL directly and do not require `--base-url`.

```powershell
# Headless execution without the default action delay
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc39_valid_login.py -o "addopts=-v --tb=short"
```

The `ui`, `api`, `integration`, `smoke`, and `regression` markers are registered for future use. No active test has a marker yet; select tests by path.

## Continuous Integration

The [Playwright Tests workflow](.github/workflows/playwright-tests.yml) runs on pushes to `main`, pull requests targeting `main`, and manual runs from the GitHub Actions tab.

- Uses Ubuntu and Python 3.12.
- Installs the pinned Python dependencies, Chromium, and its system dependencies.
- Runs TC-44 in a separate prerequisite step to create fresh credentials.
- If registration passes, runs TC-39, TC-45, TC-46, TC-42, and TC-40, with savings creation before the transfer. TC-42 contributes four cases; pytest may interleave independent tests with those variations.
- Runs Chromium headlessly, removes the local action delay, and displays printed steps. The dependent step continues after failures and returns a failing status if any case fails.

Results are available in the **Register a fresh customer** and **Run login and account-service tests** logs. If registration fails, the dependent step does not run. If TC-45 fails, TC-46 may report a missing second account; distinguish that setup consequence from a transfer defect. The local TC-42 failures and historical TC-40 result are documented above; read each CI run for its own result.

## Console Output

Use `-s` to show the printed steps. All six test functions follow the style saved in [tests/ui/AGENTS.md](tests/ui/AGENTS.md):

- Blue `◆` title banner with the test-case ID.
- Cyan `› [number]` step labels with space between steps.
- Dim, indented `↳ Expected:` descriptions.
- Green `✓ PASS` after the checks and any required save complete.
- `↻` marks a manual repeat reminder.

The formatting uses simple color constants and `print()` statements. Expected-result text describes the intended outcome; Playwright assertions enforce the implemented checks.

## Saved Test Data

TC-44 creates a unique username with `uuid` and writes `username` and `password` to `data/active_user.json` after its assertions pass. The other tests read those values. TC-40 derives an incorrect combination without changing the JSON.

The tests that read credentials resolve the JSON path relative to their own files. Registration writes relative to the working directory, so run it from the repository root. If the saved account is missing or no longer valid on the shared demo, run TC-44 again successfully, then TC-45 before a transfer test.

Registration prints the username and `Password: [hidden]`. The JSON contains synthetic demo credentials. Its path is in `.gitignore`, but the file is already tracked by Git, so updates can still appear in `git status`. Exclude regenerated credentials from progress commits.

## Reporting and Documentation

pytest supplies console results. For a TC-42 report and failure evidence after preparing saved credentials:

```powershell
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc42_val_billpay_invalid_amount.py `
    -o "addopts=-v --tb=short" --junitxml=reports/tc42.xml `
    --tracing retain-on-failure --screenshot only-on-failure --output=test-results/tc42
```

Generated reports and Playwright artifacts are ignored by Git. The command above creates local failure evidence. The current CI workflow provides console logs; report generation, trace and screenshot capture, artifact uploads, and Testiny integration are planned for CI.

- [Test strategy](docs/test-strategy.md): implemented approach and future scope.
- [Test cases](docs/test-cases.md): six implemented scenarios and planned coverage.
- [Validation record](docs/validation-2026-11-16.md): dated commands, results, and invalid-payment evidence.
- [Defect report example](docs/defect-report-example.md): an illustrative template with placeholder evidence names.

## Next Development Steps

- Automate additional invalid combinations and missing-field validation.
- Make the saved-account prerequisite part of test setup.
- Add logout, valid bill payments, and further account-service edge cases.
- Introduce page objects and shared helpers when tests need them.
- Develop API and integration tests in their placeholder directories.
- Add CI reports and failure-artifact uploads.

See [LICENSE](LICENSE) for the CC0 1.0 Universal terms.
