# data: verification

- Data tests on every model: grain (unique key), not null, accepted
  values, relationships, the `DQ-` rules.
- Reconciliation: output totals against source totals, per day.
- Backfill dry run: the backfill over a real range on a copy, with time,
  cost and a diff of the result.
- Idempotence: running the same input twice changes nothing.
- Incremental runs: a restated source day is picked up; an unchanged day
  is not re-read (both trials in this area found defects here).
