# data: requirements

Pipelines, warehouses and transformations (dbt and the like).
Extra content:

- Freshness: how late a day's data may land, per consumer.
- Completeness: what counts as a complete day, and what happens to a
  partial one.
- `DQ-` data quality rules a consumer relies on: uniqueness, not null,
  accepted values, referential rules, reconciliation against a source
  total.
- Cost per run and per backfill.

Interview prompts that pass the "no design" test:
- Who reads this data, for which decision, and how stale may it be?
- When the source restates history, what must readers see?
- Which totals must match which source, and within what tolerance?
