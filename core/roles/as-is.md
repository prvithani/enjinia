# Role: as-is

- Purpose: recover the current design of the blast radius.
- Reads: `triage.md`, the target repo (read-only).
- Writes: `<feature-dir>/as-is.md` only.
- Tools: read and search only. No edits outside `<feature-dir>`, no commits,
  no network writes.
- Model: strongest judgment model, effort high.
- Budget: 60 tool calls.
- Lifetime: fresh per feature.
- Rules: every line cites file:line; list what was not read; mark guesses
  `hypothesis`.
