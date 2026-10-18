# Concept: notifications

```yaml
invariants:
  - id: INV-1
    statement: A notification is visible only to its recipients.
    covers: [FR-1, FR-2]
    tier: property
  - id: INV-2
    statement: A notification marked read stays read across reloads and devices.
    covers: [FR-2]
    tier: example
```
