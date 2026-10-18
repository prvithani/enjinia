# database-systems: patterns

| Pattern | Earns its place when | Plain form |
|---|---|---|
| Write-ahead log | changes must survive a crash | log the change durably, then apply |
| MVCC | readers must not block writers | versions per row, visibility by snapshot |
| LSM tree | write-heavy workloads, measured | memtable, sorted runs, compaction |
| Buffer pool | working set larger than memory | fixed pages, a replacement policy, dirty tracking |
| Group commit | many small commits saturate fsync | batch commits into one fsync |
| Checkpointing | recovery must not replay the whole log | flush and record a recovery start point |
