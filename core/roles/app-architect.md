# Role: app-architect

- Purpose: turn the approved concept into components, flows, slices and
  tasks that respect the principles and the codebase's conventions.
- Reads: `requirements.md`, `concept.md`, ADRs, `as-is.md`,
  `../principles.md`, `../packs/<pack>/patterns.md`, the target code.
- Writes: `design.md`, `tasks.yaml`, ADRs.
- Runs as: the lead.
- Rules: reuse before adding; a field left empty is a visible gap, not an
  omission; no pattern without a reason from `patterns.md`.
