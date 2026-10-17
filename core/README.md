# core

Harness-free part of Enjinia: stage instructions, roles, templates, domain
packs, principles, patterns and scripts. Design: `docs/specs/enjinia/spec.md`.

Rule: nothing in `core/` names a harness or its tools. Adapters in
`adapters/<harness>/` map the abstract operations (`spawn`, `message`,
`run_layer`, `gate`, `stop`) to native tools.
