# ai-engineering: requirements

For applications built on LLMs and agents (spec section 9). Extra types:

- `BEH-` behavior spec: what a good output is, with a quality bar a grader
  can apply ("names the failing file and line", not "is helpful").
- `NFR-` cost and latency per completed task, not per call, with the model
  and effort they assume.
- `FAIL-` failure policy: what the system does when the model is wrong,
  refuses, times out or returns malformed output.

Interview prompts that pass the "no design" test:
- Show three real inputs and the output you would accept for each.
- Which wrong output is worst: a confident wrong answer, a refusal, or a
  slow answer?
- Who reads the output, and what do they do next with it?
