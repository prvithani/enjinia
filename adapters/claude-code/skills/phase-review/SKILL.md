---
name: phase-review
description: Stage 5 of the Enjinia lifecycle: full gate with evidence, trace-check through stage 5, usable check, lens review per slice and at the end.
disable-model-invocation: true
argument-hint: <feature folder> <slice>
---

Read `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.md` and
`${CLAUDE_PLUGIN_ROOT}/adapters/claude-code/operations.md`, then follow
`${CLAUDE_PLUGIN_ROOT}/core/stages/phase-review.md` for: $ARGUMENTS
For the base lenses, use the `branch-review` skill's eight lenses on the
slice diff.
