# database: patterns

| Pattern | Earns its place when | Plain form |
|---|---|---|
| Normalized core | the same fact would otherwise be stored twice | one table per entity, references by key |
| Expand and contract | a column or table changes under live traffic | add new, write both, backfill, switch reads, drop old |
| Idempotent upsert | a write can be retried | deterministic key and ON CONFLICT |
| Compare-and-swap row | concurrent writers must not overwrite newer state | WHERE version = :read-version, check the count |
| Soft delete | deleted rows are still referenced or audited | a deleted_at column and filtered reads |
| Partitioning | one table's volume or retention needs it, measured | by time or tenant, only after a measured need |
