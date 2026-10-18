# database-systems: concept

Formal tier by default. Model before code:
- Storage model and its write path, step by step, with every fsync.
- Concurrency control: what each transaction reads and writes, how
  conflicts are detected.
- Recovery: the state after a crash at every step of every write path.
- Replication: who acknowledges, what a follower may serve.

Invariants: the isolation level's forbidden anomalies never occur;
acknowledged commits survive the stated failures; recovery is
idempotent. Model each in TLA+ with a must-fail mutant per passing design
and the list of simplifications (crash points modelled, actors, bounds).
