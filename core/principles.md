# Design principles as checks

Every pack uses these. A principle is a question with a visible answer in
`design.md`. Structural checks run in `scripts/trace_check.py`; judgment
checks are the design reviewer's (`roles/design-reviewer.md`).

When two principles conflict, the ADR names the one that cuts future cost in
this codebase, and why.

| Principle | Check | Who |
|---|---|---|
| Separation of concerns, single responsibility | The component's `responsibility` is one sentence about one kind of work; its `layer` matches that work. A sentence with "and" between two kinds of work fails. | reviewer |
| Encapsulation | `exposes` lists the contract. No flow, other component or test in the design reaches past it. | reviewer |
| Dependency direction | No cycles in `depends_on`; no forbidden layer edge (pack `layers.yaml`). | trace-check |
| DRY (knowledge) | Each data entity in `owns` has one owner. The same rule or decision is not written in two components. | trace-check (owners), reviewer (rules) |
| YAGNI | Each component `realizes` a requirement or invariant. Each extension point (a protocol, multimethod, option, hook) has two users today, or one user and an ADR that names the second. | trace-check (realizes), reviewer (extension points) |
| Mechanism vs policy | A generic component (`kind: mechanism`) names no policy, user or caller in its fields. Its `second_user` field answers "if a second user appeared, would I refactor?" with the user and "no". | reviewer |
| Illegal states unrepresentable | Each invariant in `concept.md` is in some component's `enforces`, and that component's fields say how: type, constraint, or check. | trace-check (enforced), reviewer (how) |
| Conventions | A new pattern or a departure from `docs/architecture/conventions.md` has an ADR. | reviewer |

A finding follows the review rules (spec 7.3): a concrete failure, a
measured cost, or a broken rule above, with the component and field.
