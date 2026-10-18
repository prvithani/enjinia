# data: review lenses

Added to the eight base lenses:

- Lineage: every new table's sources are known and documented; nothing
  reads a table it should not.
- Idempotent backfills: a rerun or overlap gives the same result.
- Cost per run: the change's cost at full volume, estimated or measured.
- Grain: joins do not fan out rows; aggregates are at the stated grain.
