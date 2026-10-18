# database: review lenses

Added to the eight base lenses:

- Online-migration safety: no long lock or table rewrite on a large table
  while serving; backfills in batches; deploy order of code and schema.
- Index use: every new hot query uses an index; no new index without a
  query that needs it.
- Invariants in constraints: what the database can enforce, it does.
- Reversible migrations: each migration has a tested way back, or says
  why it cannot.
