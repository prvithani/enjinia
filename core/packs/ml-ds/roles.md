# ml-ds: role variants

- experimenter: runs one experiment per brief (hypothesis, split, time
  box), reports the result with its spread against the baseline, and
  records the decision. It never touches the holdout.
- eval-author (shared with ai-engineering): writes the leakage, holdout
  and slice checks from the `METRIC-` and `DATA-` requirements before
  modelling.
