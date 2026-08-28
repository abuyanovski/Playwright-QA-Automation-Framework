# Test Cases

## UI Tests

| ID | Scenario | Priority | Expected Result |
| --- | --- | --- | --- |
| UI-001 | Register a new online banking customer | High | Customer account is created and account overview is available |
| UI-002 | Log out and log back in as a registered customer | High | Customer can authenticate and view account overview |
| UI-003 | Open a new savings account | High | A new savings account number is created |
| UI-004 | Transfer funds between accounts | High | Transfer confirmation displays the correct amount and accounts |
| UI-005 | Pay a bill | High | Bill payment confirmation displays the payee and amount |

## API Tests

| ID | Scenario | Priority | Expected Result |
| --- | --- | --- | --- |
| API-001 | Retrieve account details | High | API returns account data for an authorized customer |
| API-002 | Submit a funds transfer | High | API returns a successful transfer response |
| API-003 | Submit invalid request data | Medium | API returns a validation error |

## Integration Tests

| ID | Scenario | Priority | Expected Result |
| --- | --- | --- | --- |
| INT-001 | Register customer and verify account availability through API | High | Newly registered customer data is available across layers |
| INT-002 | Complete transfer and verify updated balances | High | Balance changes reflect the completed transfer |
