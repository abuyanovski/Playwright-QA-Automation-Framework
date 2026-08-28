# Playwright-QA-Automation-Framework

QA automation framework built with Python, Playwright, and pytest.

## Project Structure

```text
Playwright-QA-Automation-Framework/
|
|-- README.md
|-- docs/
|   |-- test-strategy.md
|   |-- test-cases.md
|   `-- defect-report-example.md
|-- tests/
|   |-- ui/
|   |-- api/
|   `-- integration/
|-- pages/
|-- api/
|-- fixtures/
`-- .github/
    `-- workflows/
```

## Test Layers

- `tests/ui/`: browser-based Playwright tests.
- `tests/api/`: API-level tests.
- `tests/integration/`: workflows that verify behavior across multiple application layers.
- `pages/`: page object models for UI tests.
- `api/`: API clients and endpoint helpers.
- `fixtures/`: reusable fixture data and shared test assets.

## Tooling

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
