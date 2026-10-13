`{test}` is a Python Playwright test that reproduces a bug: it fails (exit 1) while the bug exists. dejabug has already checked that it follows the original bug video.

Port it to `@playwright/test` in TypeScript and save it as `{spec}`.

- Keep every step, in the same order, with the same video timestamps as comments.
- Use the same locators where Playwright TS has an equivalent (`getByRole`, `getByText`, `getByLabel`).
- Turn the final check into `expect(...)` assertions on the **correct** behaviour, so the spec fails while the bug exists and passes once it's fixed. Keep the failure message that explains what went wrong.
- Read the URL from `process.env.DEJABUG_URL`, falling back to `{url}`.
- Don't import anything from dejabug. The spec must run in any project with `@playwright/test`.

Then run it once to check that it fails on the bug, not on a locator or a timeout:

```
{npx} playwright test {spec_name} --config {config_name} --reporter=line
```

Iterate until the only failure is your assertion about the bug. Finish with the spec's failing assertion message.
