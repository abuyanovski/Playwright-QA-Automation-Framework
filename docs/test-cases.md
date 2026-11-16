# Test Cases

## Implemented UI Tests

| ID | Scenario | Expected result | Test file |
| --- | --- | --- | --- |
| TC-39 | Valid login using saved credentials | Authenticated navigation and Accounts Overview are visible without a login error. | [Valid login](../tests/ui/test_tc39_valid_login.py) |
| TC-40 | Login using an incorrect username and password | Login is rejected, an error appears, and account information is hidden. | [Invalid login](../tests/ui/test_tc40_invalid_login.py) |
| TC-42 | Submit empty, zero, negative, and nonnumeric bill-payment amounts | Each amount is rejected with feedback, no success confirmation, and unchanged balance and transaction history; the amount remains editable. | [Invalid bill-payment amounts](../tests/ui/test_tc42_val_billpay_invalid_amount.py) |
| TC-44 | Register a new online banking customer | Registration is confirmed, account navigation is visible, and credentials are saved. | [Account creation](../tests/ui/test_tc44_new_user_account_creation.py) |
| TC-45 | Open a savings account using an existing funding account | Confirmation appears, the new account number differs from the funding account, and its details show SAVINGS. | [Open savings account](../tests/ui/test_tc45_open_new_savings.py) |
| TC-46 | Transfer $25 between two existing accounts | Confirmation identifies the amount and accounts, balances change by exactly $25, and one new source debit appears. | [Transfer funds](../tests/ui/test_tc46_tx_funds_between_accounts.py) |

Implemented means browser actions and assertions exist, not that every scenario has a verified passing result. Discovery verified nine pytest cases across six functions: four TC-42 variations and one case for each other function. The [November 16 validation](validation-2026-11-16.md) recorded seven passes and two invalid-payment failures.

TC-39, TC-40, TC-42, TC-45, and TC-46 use credentials saved by TC-44. TC-46 also requires two accounts and at least $25 available in the first account; run TC-45 before it. Run sequentially without other activity on the same accounts.

TC-42 uses authenticated API reads to compare the source balance and transaction IDs without leaving the payment form. A zero-dollar transaction could leave the balance unchanged, so both checks are necessary. Its correction check edits the amount to 25.00 without submitting a valid payment. TC-46 compares transaction links to ensure an old transfer cannot satisfy the new-debit assertion; it does not inspect destination transaction history.

Each login test uses one credential combination; further login variations are manual or planned. TC-42's four variations are automated and receive separate pytest results.

## Planned UI Tests

The following scenarios do not have active automated tests yet.

| ID | Scenario | Priority | Expected result |
| --- | --- | --- | --- |
| UI-002 | Log out and log back in as a registered customer | High | The session ends on logout and valid credentials restore account access. |
| UI-005 | Pay a bill with a valid amount | High | Confirmation and resulting balance match the payment. |
| Planned | Additional invalid and missing-credential combinations | High | Each invalid combination is rejected with appropriate feedback. |

## Planned API Tests

`tests/api/` and `api/` currently contain placeholders.

| ID | Scenario | Priority | Expected result |
| --- | --- | --- | --- |
| API-001 | Retrieve account details | High | Authorized requests return the correct account data. |
| API-002 | Submit a funds transfer | High | A valid transfer succeeds and updates the expected accounts. |
| API-003 | Submit invalid request data | Medium | Invalid input is rejected with a validation response. |

## Planned Integration Tests

`tests/integration/` currently contains a placeholder.

| ID | Scenario | Priority | Expected result |
| --- | --- | --- | --- |
| INT-001 | Register a customer and verify account availability through the API | High | The registered customer is available across application layers. |
| INT-002 | Transfer funds and verify updated balances | High | Balance changes match the completed transfer. |
