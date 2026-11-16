# UI test output preference

The user approved the console style in `test_tc39_valid_login.py`.
Use this pattern when creating or editing UI tests in this directory.

- Keep the code beginner-friendly: simple color constants and direct `print()`
  calls beside the actions and assertions.
- Use these terminal colors and reset the color after each printed line:
  `BLUE = "\033[1;34m"`, `CYAN = "\033[36m"`, `DIM = "\033[2m"`,
  `GREEN = "\033[1;32m"`, and `RESET = "\033[0m"`.
- Start with a blue title banner showing `◆`, the test-case ID, and its name.
- Print short cyan step labels such as `› [1] Open the login page`, with a
  blank line before each step.
- Indent expected results beneath the step in dim text, prefixed with
  `↳ Expected:`. Describe the correct outcome for that scenario.
- End with a green `✓ PASS` banner only after the assertions and any required
  save operation have completed successfully.
- Mark manual repeat reminders with `↻` and the word `manual`; these reminders
  do not count as automated coverage of other data variations.
- Keep diagnostic output concise and indented. Print passwords as `[hidden]`.
- For output-only changes, preserve browser actions, assertions, test data, and
  credential-file writes. Avoid extra dependencies or logging frameworks just
  to format the output.

Use `-s` with pytest in the terminal to display the printed steps.
