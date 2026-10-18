# ml-ds: patterns

| Pattern | Earns its place when | Plain form |
|---|---|---|
| Baseline first | always | a rule or a linear model, end to end, before anything else |
| Time-based split | the model predicts the future | train on before T, evaluate on after T |
| Grouped split | rows of one entity are correlated | split by entity id, not by row |
| Feature store | many models share features and point-in-time joins | one point-in-time join function first |
| Experiment log | more than one experiment | a table: hypothesis, run id, result with spread, decision |
| Shadow deploy | a model replaces a running decision | run beside the current one, compare, then switch |

Not a pattern here: a complex model before the baseline is measured; a
pipeline framework for one notebook's work.
