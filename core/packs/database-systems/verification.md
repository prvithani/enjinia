# database-systems: verification

- Model checking of the concept's invariants.
- Deterministic simulation: the whole system in one process with simulated
  time, disk and network, so any failure replays from a seed.
- Fault injection: crashes at every write step, fsync failures, torn
  writes, network partitions.
- History checking: record concurrent operations and check the history
  for the isolation level's anomalies.
- SQL fuzzing and differential tests against a reference database.
- Standard benchmarks with a regression gate.
