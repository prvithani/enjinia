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

`backend` is the default pack. A component's `domain` field in `design.md`
selects its pack.
