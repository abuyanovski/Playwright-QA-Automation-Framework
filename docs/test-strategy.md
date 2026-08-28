# Test Strategy

## Objective

Validate critical customer workflows with maintainable automated tests using Python, Playwright, and pytest.

## Scope

- UI tests cover browser workflows through page object models.
- API tests cover service contracts and response validation.
- Integration tests cover behavior that spans multiple application layers.
- Smoke tests verify core paths quickly.
- Regression tests provide broader coverage before release.

## Tools

| Purpose | Tool |
| --- | --- |
| Test strategy | Markdown / GitHub |
| Formal test cases | Testiny |
| Test execution | Testiny |
| Automated tests | pytest + Playwright |
| Automated run results | GitHub Actions / pytest report |
| Defects | GitHub Issues |
| Source control | GitHub |
| CI | GitHub Actions |

## Test Data

Test data should be generated dynamically when possible to avoid collisions between runs. Static data belongs in `fixtures/` only when it is stable and intentionally shared.

## Execution

Run all tests:

```bash
pytest
```

Run smoke tests:

```bash
pytest -m smoke
```

Run regression tests:

```bash
pytest -m regression
```

## Reporting

Failures should include the affected workflow, reproduction steps, expected result, actual result, and supporting evidence such as screenshots, traces, logs, or API responses.
