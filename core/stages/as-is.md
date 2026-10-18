# As-is recovery (existing mode)

Role: `roles/as-is.md`, spawned read-only.
Output: `<feature-dir>/as-is.md` from `templates/as-is.md`.

Recover only the blast radius from `triage.md`:
- components: name, responsibility in one sentence, file:line, layer;
- data each one owns and the contracts between them;
- invariants the code already enforces, and where (type, constraint, check);
- invariants the code assumes but does not enforce: these are the risks;
- house patterns (errors, config, state, tests) with one example each;
- test coverage of the blast radius: which behavior is pinned, which is not.

Every line cites file:line. Anything not read is listed under "Not read".
The lead checks three citations at random before using the result.
