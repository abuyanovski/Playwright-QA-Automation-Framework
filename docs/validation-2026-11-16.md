# Local Validation: November 16, 2026

The expanded ParaBank suite completed with **7 passed, 2 failed**. Both failures showed the application processing an invalid bill-payment amount. The test assertions remain unchanged.

## Environment and Execution

- Windows; repository `.venv`; Python 3.14.10; pytest 9.1.1; pytest-playwright 0.9.0; headless Chromium.
- Public demo: `https://parabank.parasoft.com/parabank/`.
- Registration started at 08:10:57 Pacific and passed in 5.51 seconds. The dependent run started at 08:11:18 and finished with six passes and two failures in 27.27 seconds.
- Discovery collected nine cases. Browser execution verified the results below; collection alone was not treated as a pass.
- TC-44 created fresh credentials. TC-45 created the second account before TC-46 transferred funds. The tests ran sequentially without another test worker modifying the accounts.

Commands used from the repository root, with console output also saved locally:

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q -o "addopts=" -p no:cacheprovider

.\.venv\Scripts\python.exe -m pytest -s `
    tests/ui/test_tc44_new_user_account_creation.py `
    -o "addopts=-v --tb=short" `
    --junitxml=reports/prepush-registration.xml `
    --tracing retain-on-failure --screenshot only-on-failure `
    --output=test-results/prepush-registration

# Continue only after registration passes.
if ($LASTEXITCODE -ne 0) { throw "Registration failed; resolve setup before continuing." }

.\.venv\Scripts\python.exe -m pytest -s `
    tests/ui/test_tc39_valid_login.py `
    tests/ui/test_tc45_open_new_savings.py `
    tests/ui/test_tc46_tx_funds_between_accounts.py `
    tests/ui/test_tc42_val_billpay_invalid_amount.py `
    tests/ui/test_tc40_invalid_login.py `
    -o "addopts=-v --tb=short" `
    --junitxml=reports/prepush-ui.xml `
    --tracing retain-on-failure --screenshot only-on-failure `
    --output=test-results/prepush-ui
```

The registration command exited with status 0. The dependent command exited with status 1 because the two invalid-payment assertions failed. Pytest grouped TC-40 between TC-42's empty and zero variations; all four TC-42 cases still ran.

## Results

| Case | Result | Observed behavior |
| --- | --- | --- |
| TC-44 registration | Passed | Customer registration and authenticated navigation were confirmed; credentials were saved. |
| TC-39 valid login | Passed | Authenticated navigation and the account table were visible without a login error. |
| TC-45 savings creation | Passed | New account 41982 differed from funding account 41427, and its details showed SAVINGS. |
| TC-46 transfer | Passed | $25 moved from 41427 to 41982; balances changed from $415.50 to $390.50 and $100.00 to $125.00; one new source debit appeared. |
| TC-42 empty | Passed | Required-field feedback appeared; balance and transaction history stayed unchanged; the amount remained editable. |
| TC-40 invalid login | Passed | The incorrect credential combination was rejected and account information stayed hidden. |
| TC-42 zero | Failed | `0.00` produced payment confirmation and a new transaction with no balance change. |
| TC-42 negative | Failed | `-25.00` produced payment confirmation, a new transaction, and a $25 balance increase. |
| TC-42 nonnumeric | Passed | `abc` produced invalid-amount feedback; balance and transaction history stayed unchanged; the amount remained editable. |

## Invalid-Payment Evidence

Both cases filled valid payee details, selected an existing source account, entered the invalid amount, and clicked **Send Payment**. Expected behavior was rejection with amount-related feedback, no payment confirmation, and no change to account state.

### Zero amount

- Source account: 41427.
- Amount: `0.00`.
- Actual page heading: **Bill Payment Complete**; the confirmation identified the zero-dollar payment as successful.
- Balance before and after: $390.50.
- New transaction ID: 65647.

The new transaction demonstrates why a balance comparison alone would miss this invalid payment.

### Negative amount

- Source account: 41982.
- Amount: `-25.00`.
- Actual page heading: **Bill Payment Complete**; the confirmation identified the negative payment as successful.
- Balance: $125.00 before submission, $150.00 afterward.
- New transaction ID: 65980.

The selected account gained $25 when a negative bill payment was submitted.

Both tests stopped at the assertion that `#billpayResult` must be hidden. Balance and transaction diagnostics were captured first. The later rejection-feedback and input-correction assertions were not reached for these failing cases.

## Evidence and Limits

Local evidence is retained in ignored directories:

- `reports/prepush-registration.log` and `reports/prepush-registration.xml`.
- `reports/prepush-ui.log` and `reports/prepush-ui.xml`.
- `test-results/prepush-ui/`, with a failure screenshot and `trace.zip` for each failing TC-42 variation.

Generated credentials, logs, XML, screenshots, and traces are excluded from this commit. This record preserves the observations and reproduction commands; it does not publish raw browser artifacts.

These are observations from one run of a shared demo. Account numbers, balances, transaction IDs, and application behavior can change. TC-40 passed this run; its documented October 7 failure remains historical evidence, not proof of a current failure or a comprehensive login fix.

The expanded CI workflow uses Ubuntu and Python 3.12, so its result must be assessed separately from this Windows/Python 3.14 run. Test-code errors or setup failures should be distinguished from application behavior before describing any future failure as a defect.
