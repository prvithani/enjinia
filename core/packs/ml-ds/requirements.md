# ml-ds: requirements

For training and shipping models, and for data-science questions (spec
section 9). Extra types:

- `METRIC-` the target: one primary metric, its threshold, the data it is
  measured on, and the baseline it must beat. "Better" without a baseline
  is not a requirement.
- `DATA-` what data may be used: sources, time ranges, consent and privacy
  limits, what must never be a feature (the target's future, protected
  attributes).
- `NFR-` serving limits when the model ships: latency, cost per
  prediction, retraining cadence, how stale a model may get.
- `FAIL-` what happens when the model is wrong or unsure: fallback, human
  review, abstain.

Interview prompts that pass the "no design" test:
- Which decision will this model or answer change, and who makes it?
- What does a wrong prediction cost, each way (false positive, false
  negative)?
- What would you do today without a model? (That is the baseline.)
- Which data is known at the moment of the prediction, and which only
  later?
