# Stage 4: implementation

Roles: `roles/implementer.md` (one fresh agent per task),
`roles/peer-reviewer.md` (one per slice, kept for re-checks). The lead runs
the loop and owns commits.

Inputs: approved `design.md`, `tasks.yaml`, ADRs, the tests the test-author
wrote, `as-is.md` and `docs/architecture/conventions.md` where it exists.

## Before the first task (once per feature)

1. Ask the human, in one message: where the work lives (a branch in the
   target repo, or a clone when another session owns the tree); whether the
   lead commits per task after peer review (the human then reviews per
   slice) or leaves one diff per slice; how often the full review runs
   (per slice, or once at the end). Record the answers in `triage.md`.
2. Test isolation. Read how the repo's tests get their databases and
   scratch dirs. If two runs can collide (fixed database names, shared
   directories, another session on the same cluster), test runs are
   serialized: one task's tests at a time, and the full suite only when no
   other session is running it.
3. Evidence. Decide how test results become a JUnit report for
   `trace_check.py` (see the pack's `verification.md`). Never change the
   repo's runner for this; wrap the run instead.
4. If commits are approved: the first commit holds the test-author's tests
   and any runner registration, before any code.

## Per slice, in order (S0 first)

For each layer of the slice's tasks (`trace_check.py <feature-dir>` prints
the layers):

1. For each task in the layer, `spawn(implementer, brief)`. Tasks in one
   layer run in parallel only in separate worktrees (one per task, placed
   where the repo's relative paths resolve); in one shared tree they run
   one after another, because each one's test runs would include the
   others' half-made edits.
   Brief: the task card from `tasks.yaml`; the design sections it `reads`;
   the invariants it covers; the exact contracts the tests assume (names,
   arguments, return shapes), copied from the test-author's report; the
   test namespaces to run and the command; the conventions; the pattern
   named in `design.md` for its component, or "none".
2. When the implementer reports, the lead reruns the task's tests itself.
   A report is not evidence.
3. `spawn` or `message` the slice's peer-reviewer with the diff of this
   task only, the task card and the design sections. At most 3 rounds of
   fix and re-check; then `gate` with both positions.
4. Commit (if approved): one commit per task, explicit paths, the repo's
   message conventions.

Rules for every task:
- The implementer never edits tests written by the test-author. A test it
  cannot pass is raised to the peer-reviewer and the lead with the reason.
- A pattern or abstraction not named in `design.md` is raised, not added.
- Existing mode: if the slice is a refactor, it changes no behavior; its
  tests and the existing suite must stay green.
- Format and lint as the repo requires before review.

Gate: none per task beyond the peer review. The slice gate is stage 5.
