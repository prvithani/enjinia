# ml-ds: verification

- Holdout: an evaluation set fixed before modelling starts and used only
  for the final numbers. Tuning uses a separate validation split.
- Leakage checks in code: features against the moment of prediction;
  overlap between train and evaluation rows (ids, near-duplicates, the
  same entity across splits).
- Metric with uncertainty: every reported number has its spread (seeds,
  bootstrap or cross-validation), and the baseline's number beside it.
- Slices: the metric on the subgroups the decision cares about, not only
  overall.
- Reproducibility: data version, code commit, seed and environment
  recorded per run; one run is re-done from the record before the result
  is accepted.
- When the model ships: a regression check on the holdout for every
  retrain, and monitoring of input drift and of the metric once labels
  arrive.

Evidence for trace_check: requirements map to checks (leakage, holdout
metric, slice metrics) written as tests with `covers` metadata. Python
projects need a pytest `covers` reader in trace_check before this pack's
first real run; it reads Clojure `deftest` metadata only today.
