# Test Strategy

## Objective

Validate ParaBank registration and login with clear Python, Playwright, and pytest tests while keeping the project simple as coverage develops.

## Current Scope

- TC-44 registers a unique customer, checks confirmation and authenticated navigation, and saves credentials.
- TC-39 uses saved credentials and checks authenticated navigation, the absence of a login error, and the Accounts Overview URL and table.
- TC-40 submits incorrect variants of the saved credentials and checks for rejected login, a visible error, and hidden account information.

Each login test currently uses one credential combination. Manual repeat reminders in the output do not automate additional variations.

The tests use direct Playwright calls and the `page` fixture from pytest-playwright. Unused page objects, generators, and custom fixtures have been removed. `pages/`, `utils/`, `fixtures/`, `api/`, API/integration test directories, and the CI directory are placeholders for later work.

## Planned Scope

- Additional invalid and missing-credential cases.
- Logout and account-service workflows, including balance verification.
- Reusable account setup, fixtures, and page objects when needed.
- API service checks, cross-layer integration tests, and CI.
- Smoke/regression classification and reporting integrations.

## Test Data

TC-44 generates a unique username with `uuid` and saves synthetic demo credentials to `data/active_user.json` after its assertions pass. TC-39 reads them; TC-40 adds `_invalid` to both fields.

Run registration from the repository root before the login tests. An account saved in JSON may need regeneration if the public demo's state changes. Passwords are hidden in the printed output.

## Execution

Use the project's virtual environment and the [README commands](../README.md#running-the-tests). The full workflow specifies TC-44 before TC-39 and TC-40; generic discovery does not establish this dependency.

Use `--collect-only` to verify discovery without browser actions and `-s` to display the numbered, colored steps. The output convention is recorded in [tests/ui/AGENTS.md](../tests/ui/AGENTS.md).

Markers are registered in `pytest.ini` but are not applied to the active tests. Select tests by file path.

## Reporting

pytest provides console results and optional JUnit XML. Playwright can retain failure traces and screenshots when requested. CI, automated uploads, and Testiny integration are planned.

Record the affected scenario, reproduction steps, expected and actual results, and supporting evidence when investigating a failure. The shared demo previously authenticated with incorrect credentials in a local TC-40 run; this needs investigation and is not counted as a passing rejection check.
