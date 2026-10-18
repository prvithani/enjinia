---
name: design-review
description: Review a Enjinia design.md against the principles before code exists, with a fresh-context reviewer.
disable-model-invocation: true
argument-hint: <feature folder>
---

Spawn a fresh reviewer as in
`${CLAUDE_PLUGIN_ROOT}/adapters/claude-code/operations.md`, with the role
`${CLAUDE_PLUGIN_ROOT}/core/roles/design-reviewer.md` and the principles
`${CLAUDE_PLUGIN_ROOT}/core/principles.md`, on the feature folder:
$ARGUMENTS
Report its table unchanged, then the trace-check result for stage 3.
