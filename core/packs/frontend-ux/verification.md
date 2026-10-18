# frontend-ux: verification

- Interaction tests in a real browser (Playwright or the repo's runner)
  for each flow, including error and slow paths.
- Visual regression on the changed screens.
- Accessibility audit: automated (axe or similar) plus a keyboard-only
  walk-through of each flow.
- Browser suites isolate their data: own database, ports and data
  directories; respect a suite's "CI only" guard.
