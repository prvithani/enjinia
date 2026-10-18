# database: requirements

Schema, SQL and migrations inside an application (spec section 9); used by
backend and data work. Extra content:

- Access patterns: each query the feature adds or changes, its frequency,
  and its latency bound at a stated data volume.
- Volume and growth: rows now and in a year, per table touched.
- Retention: how long rows live, what deletes them, what must never be
  deleted.
- `EB-` for every existing reader of a changed table or column.

Interview prompts that pass the "no design" test:
- Which question must the data answer, how often, how fast?
- What may be lost, duplicated or late, and for how long?
- What exists today that this changes? (Rows, ids, saved references,
  fixtures.)
