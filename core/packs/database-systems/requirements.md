# database-systems: requirements

Building a database engine: storage, transactions, recovery, replication.
Extra content:

- Workload mix: read/write ratio, transaction sizes, key distribution,
  concurrency, at stated scales.
- Isolation level, stated by its anomalies (which must never happen).
- Durability guarantee: what survives a process crash, an OS crash, a
  power loss, a disk loss; when a commit is acknowledged.
- Protocol and format compatibility: wire protocol, SQL dialect, on-disk
  format versions that must still be read.
