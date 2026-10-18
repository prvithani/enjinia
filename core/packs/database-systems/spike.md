# database-systems: spike

- Microbenchmark of one path (a page write, a lookup, a commit) on the
  target hardware, with the variance across runs.
- An I/O cost model: page reads and writes per operation, write
  amplification, fsyncs per commit; checked against a measurement.
