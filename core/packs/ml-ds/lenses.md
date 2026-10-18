# ml-ds: review lenses

Added to the eight base lenses:

- Leakage: any feature, join or aggregation that can see the future or the
  label.
- Evaluation contamination: the holdout touched during tuning, model
  selection or feature design.
- Reproducibility: the result can be re-run from what is recorded.
- Baseline and spread: every claimed gain is against the baseline, with
  its uncertainty.
- Metric fit: the metric matches the cost of the decision; slices checked.
