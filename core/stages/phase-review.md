# Stage 5: review

Per slice, after its last task, and once more after the last slice.

1. The repo's full gate, as the conventions name it (all test suites,
   format and lint checks). Before running each suite, read how it isolates
   itself (databases, ports, data directories, guards like "CI only") and
   give it its own, so it cannot touch another session's or a real
   workspace's data; ask the human before overriding a guard. Run it with the evidence wrapper
   (`stages/implement.md`, before the first task, step 3) and paste the
   summary. Serialized if test runs can collide.
2. `trace_check.py <feature-dir> --stage 5 --tests <dirs> --report <junit>`:
   every requirement of the slice has passing evidence.
3. Usable check: write in one paragraph what a user can do after this slice
   that they could not before, and confirm it from the tests or by running
   it.
4. Review. The eight base lenses (correctness, crash-safety, reuse, tests,
   performance, complexity, docs, design; the adapter names its tool for
   them) plus the lenses of every pack in the slice, on the slice's diff,
   each a fresh read-only reviewer. Frequency per the human's answer in
   `triage.md`. Review rules: spec 7.3.
5. Fix findings through stage 4's loop; the same reviewers re-check.

Final review (after the last slice), in addition:
- every row of the traceability matrix complete;
- every invariant has a test at its tier;
- each responsibility lives in the component the design gives it;
- every deviation from `design.md` has an ADR;
- existing mode: every `EB-` row pinned by a passing test.

Gate: the human approves the final review. The human commits or pushes;
agents never push.
