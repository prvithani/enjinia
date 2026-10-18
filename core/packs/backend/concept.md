# backend: concept

The concept artifact: actors, state, operations, invariants (`INV-n`) with
a verification tier.

- `formal` when correctness depends on interleavings: concurrent writers,
  crash and retry, ordering at boot, publish protocols. Model with TLA+
  (`core/scripts/tlc`); for each passing design, run one must-fail mutant;
  list every simplification that fixes something the real system varies.
- `property` for pure logic with a rule over many inputs (choosers,
  parsers, merges).
- `example` for the rest.

Both trials found their key defect at this stage: a stale merge base
(upsert-fence) and an ordering requirement a database constraint cannot
give (workspace-date-column).
