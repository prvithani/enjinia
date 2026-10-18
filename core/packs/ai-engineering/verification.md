# ai-engineering: verification

Evals are the tests of a model's behavior.

- A case is an input plus a way to grade the output: code (exact or
  structural checks), a model grading against a written rubric, or a
  human. Prefer code; use a model grader only where code cannot judge.
- Every role has a regression eval, run on every prompt, model, effort or
  harness change. A change ships only if the eval does not get worse.
- Seeded defects: inputs with a known defect the role must catch, plus
  clean inputs that must produce nothing (measures misses and noise).
  Example: `core/evals/design-review/`.
- Cost and latency are measured per completed task from logged usage.
- Prompt-injection cases: inputs that carry instructions the role must
  treat as data.
- Model graders are themselves checked: a sample of their grades against a
  human's.
