# Test Cases

## Implemented UI Tests

| ID | Scenario | Expected result | Test file |
| --- | --- | --- | --- |
| TC-39 | Valid login using saved credentials | Authenticated navigation and Accounts Overview are visible without a login error. | [Valid login](../tests/ui/test_tc39_valid_login.py) |
| TC-40 | Login using an incorrect username and password | Login is rejected, an error appears, and account information is hidden. | [Invalid login](../tests/ui/test_tc40_invalid_login.py) |
| TC-44 | Register a new online banking customer | Registration is confirmed, account navigation is visible, and credentials are saved. | [Account creation](../tests/ui/test_tc44_new_user_account_creation.py) |

Implemented means browser actions and assertions exist, not that every scenario has a verified passing result. TC-39 and TC-40 require the JSON account saved by TC-44. Each login test uses one combination; further variations are manual or planned.

## Planned UI Tests

The following scenarios do not have active automated tests yet.

| ID | Scenario | Priority | Expected result |
| --- | --- | --- | --- |
| UI-002 | Log out and log back in as a registered customer | High | The session ends on logout and valid credentials restore account access. |
| UI-003 | Open a new savings account | High | A new savings account number is created. |
| UI-004 | Transfer funds between accounts | High | Confirmation and resulting balances match the transfer. |
| UI-005 | Pay a bill | High | Confirmation and resulting balance match the payment. |
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
