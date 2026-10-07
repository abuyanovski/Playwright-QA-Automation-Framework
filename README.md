# Playwright QA Automation Framework

A QA automation portfolio built with Python, Playwright, and pytest. The current focus is three browser tests against the public ParaBank demo: customer registration, valid login, and invalid login.

**Status: work in progress.** These scenarios have automated actions and assertions. Their presence does not establish a fully passing baseline against the shared demo site.

## Current Tests

| Test case | File | What it checks |
| --- | --- | --- |
| TC-44: Account creation | [test_tc44_new_user_account_creation.py](tests/ui/test_tc44_new_user_account_creation.py) | Registers a unique customer, checks registration confirmation and account navigation, then saves credentials. |
| TC-39: Valid login | [test_tc39_valid_login.py](tests/ui/test_tc39_valid_login.py) | Reads saved credentials and checks authenticated navigation, no visible login error, the Accounts Overview URL, and the account table. |
| TC-40: Invalid login | [test_tc40_invalid_login.py](tests/ui/test_tc40_invalid_login.py) | Adds `_invalid` to the saved username and password, submits them, and checks that login is rejected, an error is visible, and account information is hidden. |

Each login test currently uses one credential combination. The printed Step 8 is a manual repeat reminder; additional data variations and missing-field cases are not automated yet.

TC-40 expects rejection. A previous local run of the public demo opened Accounts Overview after incorrect credentials were submitted, so a failing rejection check needs investigation.

## Project Structure and Cleanup

Unused page objects, customer/payee fixtures, and separate data generators have been removed. Test filenames now use consistent underscores without spaces or hyphens. Dependencies are limited to those used by the active tests.

Directories reserved for future work contain only `.gitkeep` placeholders. Their names describe planned areas, not implemented capabilities.

```text
.github/
    workflows/.gitkeep                  Future CI workflows
api/.gitkeep                            Future API clients
data/
    active_user.json                    Saved demo credentials
docs/
    README.md                          Documentation index
    test-cases.md                      Current and planned coverage
    test-strategy.md                    Current approach and future scope
    defect-report-example.md            Illustrative report template
fixtures/.gitkeep                       Future reusable test data/fixtures
pages/.gitkeep                          Future page objects
tests/
    ui/
        AGENTS.md                      Preferred console output style
        test_tc39_valid_login.py
        test_tc40_invalid_login.py
        test_tc44_new_user_account_creation.py
    api/.gitkeep                        Future API tests
    integration/.gitkeep                Future integration tests
utils/.gitkeep                          Future shared helpers
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

Run registration successfully before either login test to create fresh `data/active_user.json` credentials:

```powershell
# TC-44: register and save credentials
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc44_new_user_account_creation.py

# TC-39: valid login
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc39_valid_login.py

# TC-40: invalid login
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc40_invalid_login.py
```

To run all three in registration-first order and stop at the first failure:

```powershell
.\.venv\Scripts\python.exe -m pytest -s -x `
    tests/ui/test_tc44_new_user_account_creation.py `
    tests/ui/test_tc39_valid_login.py `
    tests/ui/test_tc40_invalid_login.py
```

A plain `pytest` run discovers all three tests but does not arrange their credential dependency. Prepare saved credentials first or use the ordered command above.

To inspect discovery without opening browsers:

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

If an existing PyCharm run configuration points to an old filename, recreate it using the Run icon beside the test in its renamed file.

[pytest.ini](pytest.ini) defaults to verbose output, short tracebacks, a visible browser, and a 500 ms action delay (`--headed --slowmo 500`). All three tests hardcode the public ParaBank URL and do not require `--base-url`.

```powershell
# Headless execution without the default action delay
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc39_valid_login.py -o "addopts=-v --tb=short"
```

The `ui`, `api`, `integration`, `smoke`, and `regression` markers are registered for future use. No active test has a marker yet; select tests by path.

## Console Output

Use `-s` to show the printed steps. All three tests follow the style saved in [tests/ui/AGENTS.md](tests/ui/AGENTS.md):

- Blue `◆` title banner with the test-case ID.
- Cyan `› [number]` step labels with space between steps.
- Dim, indented `↳ Expected:` descriptions.
- Green `✓ PASS` after the checks and any required save complete.
- `↻` marks a manual repeat reminder.

The formatting uses simple color constants and `print()` statements. Expected-result text describes the intended outcome; Playwright assertions enforce the implemented checks.

## Saved Test Data

TC-44 creates a unique username with `uuid` and writes `username` and `password` to `data/active_user.json` after its assertions pass. TC-39 reads those values directly. TC-40 reads them and derives an incorrect combination without changing the JSON.

Both login tests resolve the JSON path relative to their own files. Registration writes relative to the working directory, so run it from the repository root. If the saved account is missing or no longer valid on the shared demo, run TC-44 again successfully.

Registration prints the username and `Password: [hidden]`. The JSON contains synthetic demo credentials. Its path is in `.gitignore`, but the file is already tracked by Git, so updates can still appear in `git status`.

## Reporting and Documentation

pytest supplies console results. For a login report and failure evidence after preparing saved credentials:

```powershell
.\.venv\Scripts\python.exe -m pytest -s tests/ui/test_tc39_valid_login.py `
    --junitxml=reports/junit.xml --tracing retain-on-failure --screenshot only-on-failure
```

Generated reports and Playwright artifacts are ignored by Git. Traces and screenshots require the options above. The CI directory is a placeholder; automated uploads and Testiny integration are planned.

- [Test strategy](docs/test-strategy.md): implemented approach and future scope.
- [Test cases](docs/test-cases.md): three current scenarios and planned coverage.
- [Defect report example](docs/defect-report-example.md): an illustrative template with placeholder evidence names.

## Next Development Steps

- Automate additional invalid combinations and missing-field validation.
- Make the saved-account prerequisite part of test setup.
- Add logout, account-service scenarios, and balance assertions.
- Introduce page objects and shared helpers when tests need them.
- Develop API, integration, and CI capabilities in their placeholder directories.

Tests depend on the availability and state of the shared ParaBank demo. Investigate failures before recording a passing baseline.

See [LICENSE](LICENSE) for the CC0 1.0 Universal terms.
