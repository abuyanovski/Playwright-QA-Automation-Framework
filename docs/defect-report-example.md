# Defect Report Example

## Summary

Transfer confirmation displays the wrong destination account after submitting a valid funds transfer.

## Environment

- Application: Parabank
- Browser: Chromium
- Test type: UI regression
- Build: test environment

## Preconditions

- Customer is registered.
- Customer has at least two active accounts.

## Steps To Reproduce

1. Log in as a registered customer.
2. Open the transfer funds page.
3. Enter `25.00` as the transfer amount.
4. Select a source account.
5. Select a different destination account.
6. Submit the transfer.

## Expected Result

The confirmation message displays the selected destination account.

## Actual Result

The confirmation message displays a different destination account.

## Severity

High

## Evidence

- Screenshot: transfer-confirmation.png
- Trace: transfer-confirmation.zip
