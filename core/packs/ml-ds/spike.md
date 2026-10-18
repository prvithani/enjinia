# ml-ds: spike

The spike is an experiment: one hypothesis ("feature X lifts recall at
fixed precision"), a fixed time box, a run on the agreed split, the result
against the baseline with its spread (seeds or bootstrap), and a decision
recorded in the experiment log (`<feature-dir>/experiments.md`): keep,
drop, or test further. A result without its spread is a hypothesis, not a
measurement.
