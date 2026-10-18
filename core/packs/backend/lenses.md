# backend: review lenses

Added to the eight base lenses:

- Concurrency: every shared write has an owner, a fence or a lock; boot
  and request paths are ordered as the concept says.
- API contract compatibility: callers of every changed contract still get
  what they relied on (shapes, errors, ids).
- Idempotent retries: every step that can run twice after a crash leaves
  the same state.
