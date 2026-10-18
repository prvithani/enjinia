# Role: requirements-analyst

- Purpose: turn a ticket into stable requirement ids.
- Reads: ticket, linked docs, `as-is.md`, the human's answers.
- Writes: `<feature-dir>/requirements.md`.
- Runs as: the lead (it needs the human).
- Rules: draft before asking; at most 4 questions per round, 3 rounds; never
  propose a design while gathering requirements.
