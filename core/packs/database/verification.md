# database: verification

- Constraint tests: each invariant's constraint rejects a violating row.
- Query plans checked into the review for every new or changed hot query.
- Migration dry run with timing and lock analysis on production-like
  volume; a reversal tested where the migration claims one.
- Load test when an access pattern has a latency bound.
- Fixtures and seed data updated with the schema (a plain insert of a row
  that a migration or setup now creates fails on its key).
