# data: concept

- The data model: grain of each table (one row is what), keys, and the
  facts and dimensions it holds.
- Lineage: which sources and transformations feed each table.
- Data contracts at each boundary: columns, types, keys, freshness and
  quality rules the producer promises.

Invariants worth stating: each table's grain holds (no duplicate key
rows); a rerun or backfill of the same input gives the same output
(idempotent); totals reconcile with the source within the stated
tolerance. Incremental state (what was already read, versions, seen
items) usually earns the formal tier: two trials found defects there.
