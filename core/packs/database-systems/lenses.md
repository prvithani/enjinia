# database-systems: review lenses

Added to the eight base lenses:

- Crash consistency of every write path: what a crash at each step
  leaves, and that recovery handles it.
- On-disk format compatibility: old files are still read; format changes
  are versioned.
- Latch and lock ordering: one global order, no lock held across I/O
  without a reason.
- Benchmark regression gate: the change's effect on the standard
  benchmarks, measured.
