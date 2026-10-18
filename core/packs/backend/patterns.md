# backend: patterns

When a pattern earns its place, and its plain form. A pattern is named in a
component's `pattern` field with a reason; an implementer that needs one not
named raises it instead of adding it (spec 7.2).

The plain form comes first. Use the named form only when the plain one has
failed twice in this codebase.

| Pattern | Earns its place when | Plain form (Clojure) | Plain form (Python) |
|---|---|---|---|
| Strategy | two or more behaviors are chosen at run time, today | a map of keyword to fn; a multimethod if callers extend it | a dict of name to function |
| Adapter | an external API's shape differs from the domain's and more than one caller uses it | one namespace of plain fns translating at the boundary | one module of functions |
| State machine | an entity has states whose allowed transitions matter (invariants name them) | a transition map `{state {event next-state}}` and one `step` fn | a dict of dicts and one `step` |
| Registry | components are added without editing a central list | a map populated at load; refuse duplicate keys | a dict with a register function |
| Outbox | a database write and a message must both happen or neither | an outbox table written in the same transaction, drained by one worker | same |
| Compare-and-swap | concurrent writers must not overwrite each other's newer state | a conditional update `WHERE version = :read-version`, check the row count | same |
| Idempotent operation | a step can run twice after a crash or retry | a deterministic id and `ON CONFLICT DO NOTHING` / upsert | same |
| Protocol (interface) | two implementations exist today | defprotocol with both implementations | `typing.Protocol` |

Not a pattern here: a protocol with one implementation, a factory for one
product, a config value that never changes. These fail YAGNI in
`../../principles.md`.
