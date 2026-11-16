# Test Strategy

## Objective

Validate ParaBank registration, login, invalid bill payments, savings-account creation, and transfers with clear Python, Playwright, and pytest tests.

## Current Scope

- TC-44 registers a unique customer, checks confirmation and authenticated navigation, and saves credentials.
- TC-39 uses saved credentials and checks authenticated navigation, the absence of a login error, and the Accounts Overview URL and table.
- TC-40 submits incorrect variants of the saved credentials and checks for rejected login, a visible error, and hidden account information.
- TC-42 checks four invalid payment amounts, validation feedback, unchanged balance and transaction history, and the ability to edit the amount after rejection.
- TC-45 opens a savings account and checks confirmation, the new account number, and the account type.
- TC-46 transfers $25, checks both balance changes using Decimal, and verifies one new source-account debit.

Each login test currently uses one credential combination. Manual repeat reminders in the output do not automate additional variations.

The six test functions use direct Playwright calls and the `page` fixture from pytest-playwright. TC-42 is parameterized into four cases, giving nine collected cases overall. It uses authenticated API reads to compare account state without navigating away from Bill Pay. This supporting check does not constitute a standalone API test suite.

`pages/`, `utils/`, `fixtures/`, `api/`, and API/integration test directories contain placeholders for later work. GitHub Actions runs the implemented UI scenarios in prerequisite order.

## Planned Scope

- Additional invalid and missing-credential cases.
- Logout, valid bill payments, and additional account-service edge cases.
- Reusable account setup, fixtures, and page objects when needed.
- Standalone API service checks and cross-layer integration tests.
- Smoke/regression classification and reporting integrations.

## Test Data

TC-44 generates a unique username with `uuid` and saves synthetic demo credentials to `data/active_user.json` after its assertions pass. The other tests read them; TC-40 adds `_invalid` to both fields.

Run registration from the repository root before the remaining tests. TC-45 creates the second account required by TC-46, whose first account needs at least $25 available. An account saved in JSON may need regeneration if the public demo's state changes. Run sequentially without concurrent changes to the same accounts. Passwords are hidden in the printed output, and generated credential changes are excluded from commits.

## Execution

Use the project's virtual environment and the [README commands](../README.md#running-the-tests). Run TC-44 as a prerequisite, then select TC-39, TC-45, TC-46, TC-42, and TC-40 in that order. Generic discovery does not establish these dependencies. Keep account-changing positive scenarios ahead of TC-42 so an incorrectly processed invalid payment does not affect their starting state. Pytest may interleave independent tests with TC-42's parameterized cases; in the recorded local run, TC-40 ran between the empty and zero cases.

CI uses a separate registration step. If registration fails, the dependent test step does not run. Otherwise, the remaining cases run without fail-fast behavior so each case can report its result. A TC-45 failure may leave TC-46 without its second-account prerequisite; classify that as a setup consequence when reviewing results.

Use `--collect-only` to verify discovery without browser actions and `-s` to display the numbered, colored steps. The output convention is recorded in [tests/ui/AGENTS.md](../tests/ui/AGENTS.md).

Markers are registered in `pytest.ini` but are not applied to the active tests. Select tests by file path.

## Reporting

pytest provides console results and optional JUnit XML. Playwright can retain failure traces and screenshots when requested. CI currently provides console logs; automated artifact uploads and Testiny integration remain planned.

Record the affected scenario, reproduction steps, expected and actual results, and supporting evidence when investigating a failure. Keep assertions strict when the application violates the expected behavior. Report application defects separately from test-code errors and setup failures, and do not count discovery as a passing execution. The [README](../README.md) records dated results, including the previously observed TC-40 login defect.
