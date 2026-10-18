# Stage 3: application design

Role: `roles/app-architect.md`, run by the lead.
Inputs: approved `requirements.md`, `concept.md`, accepted ADRs, `as-is.md`.
Output: `<feature-dir>/design.md` from `templates/design.md`, ADRs,
`<feature-dir>/tasks.yaml` from `templates/tasks.yaml`, tests.

1. Components. For each: the fields in the template. Existing mode: reuse
   the components in `as-is.md` by name; a new component needs a reason.
   Follow `docs/architecture/conventions.md` of the target repo where it
   exists, and `as-is.md` house patterns otherwise.
2. Every invariant in `concept.md` gets a component that `enforces` it, with
   how (type, constraint, check). An invariant no component enforces is a gap.
3. Patterns: name one in `pattern` only if `packs/<pack>/patterns.md` says it
   earns its place; write the reason. Otherwise `none`.
4. Flows: one numbered sequence per main flow. Existing mode: mark each step
   new, changed or unchanged.
5. Slices: each usable on its own. The first is the walking skeleton. In
   existing mode, refactoring the touched code to the principles comes first
   as its own slice; behavior changes after it.
6. Tasks: one per unit of work in `tasks.yaml`; `depends_on` forms a graph
   (no cycles); every requirement and invariant is covered by a task.
7. Run `trace_check.py <feature-dir> --stage 3`. Structural gaps (cycles,
   layers, owners, realizes) are fixed before review.
8. Design review: `spawn(design-reviewer, brief)` with `design.md`,
   `concept.md`, `requirements.md`, `../principles.md` and the ADRs. Fix or
   answer each finding; the same reviewer re-checks (`message`). At most 3
   rounds, then `gate` with both positions.
9. Tests: `spawn(test-author, brief)` after the review passes. Then run the
   tests on the current code: tests for new behavior must fail, tests for
   `EB-` rows must pass. A new-behavior test that passes today tests
   nothing; send it back.
10. Run `trace_check.py <feature-dir> --stage 3 --tests <dir>` and report.

Gate: the human approves `design.md`, `tasks.yaml` and the test list. At L2
the lead approves this gate itself and logs it as an `auto` ADR.
