---
name: lifecycle
description: Run a ticket, request or review finding through Enjinia's engineering lifecycle (triage, requirements, conceptual design with model checking). Use when asked to run enjinia or the lifecycle on a ticket.
disable-model-invocation: true
argument-hint: <ticket id, finding, or request>
---

Read `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.md` and
`${CLAUDE_PLUGIN_ROOT}/adapters/claude-code/operations.md`, then run the
lifecycle on: $ARGUMENTS

Start with `${CLAUDE_PLUGIN_ROOT}/core/stages/triage.md`. Templates are in
`${CLAUDE_PLUGIN_ROOT}/core/templates/`, roles in
`${CLAUDE_PLUGIN_ROOT}/core/roles/`.
