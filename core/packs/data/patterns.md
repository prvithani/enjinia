# data: patterns

| Pattern | Earns its place when | Plain form |
|---|---|---|
| Dimensional model | analysts slice facts by many attributes | fact tables at a stated grain, dimension tables by key |
| Staging, then marts | sources need cleaning before modelling | one staging layer per source, typed and renamed only |
| Incremental by partition | full rebuilds cost too much, measured | replace whole partitions (days), never merge rows ad hoc |
| Snapshot (SCD type 2) | readers need history of a changing attribute | valid_from and valid_to per row |
| Upsert by key | a source restates rows | merge on the key, latest wins, with a seen-version fence |
| Spine | facts from several feeds must line up without loss | a complete set of (date, keys) rows, each feed left-joined |
