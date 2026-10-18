# Domain packs

A pack specializes the lifecycle for one domain (`spec.md` section 9). Every
pack has the same slot files:

| File | Slot |
|---|---|
| `requirements.md` | extra requirement types and their ID prefixes |
| `concept.md` | the concept artifact for this domain |
| `spike.md` | spike kinds |
| `verification.md` | verification tiers and checks |
| `lenses.md` | review lenses added to the base lenses |
| `patterns.md` | patterns and their plain form |
| `roles.md` | role variants |
| `layers.yaml` | layer names a component may declare, and forbidden dependencies (read by `scripts/trace_check.py`) |

Packs: `backend` (the default), `ai-engineering`, `database`, `data`,
`frontend-ux`, `database-systems`, `ml-ds` (spec section 9). Only backend
has run on real work; ai-engineering on Enjinia's own evals. The others are
written from the spec and the trials' lessons, and should be tightened on
their first real ticket.

`backend` is the default pack. A component's `domain` field in `design.md`
selects its pack.
