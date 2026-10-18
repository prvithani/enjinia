# ai-engineering: concept

The concept artifact:
- For each step: plain code or an agent. Code decides control flow,
  retries, gates and stopping; a model makes judgments inside a role.
- Roles: purpose, inputs (file pointers, never transcripts), output
  schema, tools, model and effort, budget, lifetime.
- Tool surface per role, least privilege.
- Failure modes and the defense for each (see `lenses.md`).

Invariants worth stating: every model output that code consumes is
validated against a schema; no role sees content it must not act on
(prompt injection); the orchestrator's next step never depends on
unvalidated model text.
