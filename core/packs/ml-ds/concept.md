# ml-ds: concept

The concept artifact frames the problem before any model:
- The prediction or question, the unit (one row is what?), and the moment
  of prediction (what is known then).
- The primary metric and why it matches the decision's cost; secondary
  metrics that must not get worse.
- The baseline: the rule or simple model that ships if nothing beats it.
- Data and labels: sources, how labels are made, their delay and noise,
  the split that matches how the model will be used (by time when the
  future is predicted).

Invariants worth stating (tier `property` or `example`, checked in code):
- No row's features use information from after its moment of prediction
  (no leakage).
- No row of the evaluation data was seen in training or tuning.
- A run is reproducible from its recorded data version, code and seed.

Shape of the lifecycle here (spec section 9): experiment-driven. The first
slice is a walking skeleton: the baseline end to end (data, features,
model, evaluation, and serving if it ships). Then measured iterations,
each one a hypothesis, a run and a recorded decision. A question whose
deliverable is an answer, not a model, runs as an investigation:
question, method, evidence, answer, with the same gates.
