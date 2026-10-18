# database: spike

- Query plan on realistic volume: generate or copy data at the stated
  volume, run EXPLAIN (ANALYZE) on each new or changed query, record the
  plan and timing.
- Migration rehearsal on a copy: time it, record the locks it takes and
  for how long, and whether it rewrites the table.
- What a statement actually does under conflict or concurrency, when the
  docs leave it open.
