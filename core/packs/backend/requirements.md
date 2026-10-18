# backend: requirements

Extra requirement types for backend work, on top of the lifecycle's
`BR- FR- NFR- TR- G- NG- EB-`:

- `NFR-` with a number: latency (p50/p99 at a stated load), throughput,
  data volume and growth, freshness. A number without its load is not a
  requirement.
- `EB-` for every contract other code depends on: API shapes, stored
  formats, denial reasons, ids derived from other ids.

Interview prompts that pass the "no design" test:
- What may callers observe, and what must they never observe?
- Under a crash or a retry, what is the worst acceptable outcome (late,
  twice, fail and retry by hand)?
- What exists today that this changes? (Deployed data shapes, saved ids,
  fixtures.)
