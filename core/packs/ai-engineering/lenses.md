# ai-engineering: review lenses

Added to the eight base lenses:

- Context hygiene: each role gets only the files it needs; no transcripts
  passed between roles.
- Cache-friendly prompts: stable content (role rules, spec) first,
  volatile content (the task) last.
- Least-privilege tools: a reviewer is read-only; nothing pushes.
- Validated structured output: every output code consumes has a schema and
  is checked; a failure is handled, not retried blindly.
- Deterministic orchestrator: stages, gates and retries are code, testable
  without a model.
- Eval coverage: every role has cases, and the eval ran on this change.
