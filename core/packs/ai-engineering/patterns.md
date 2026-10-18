# ai-engineering: patterns

From "Building effective agents" (Anthropic), plain form first.

| Pattern | Earns its place when | Plain form |
|---|---|---|
| Prompt chaining | a task splits into fixed steps whose outputs feed each other | sequential calls with a check between them |
| Routing | inputs fall into kinds that need different prompts or models | a classifier step, then a map from kind to role |
| Parallelization | independent subtasks, or several views of one input (lenses) | parallel role runs, results merged by code |
| Orchestrator-workers | subtasks are not known in advance | a lead plans, workers run, the lead merges |
| Evaluator-optimizer | a written rubric can judge the output and revision helps | generate, grade, revise, with a round cap |
| Role runner | one boundary for every role, so vendors and harnesses can change | `run_role(role, brief, files, budget)` |

Not a pattern here: an agent loop where a single call works; a multi-agent
design where one agent fits in its context.
