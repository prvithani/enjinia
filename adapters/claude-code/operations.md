# Claude Code operations

How the Claude Code adapter runs the abstract operations in
`core/lifecycle.md`.

- `spawn(role, brief)`: Agent tool, `subagent_type: general-purpose`. The
  prompt is the role file's text, then the brief (file pointers, the
  feature folder, the stop conditions). Name the model from the role file.
  State in the prompt: no commits, no pushes, no edits outside the feature
  folder unless the role allows them.
- `message(agent, text)`: SendMessage to the agent's id.
- `run_layer(tasks)`: one Agent call per task in the same response; the
  Workflow tool only when the human asked for workflows.
- `gate(question)`: AskUserQuestion when the answer is a choice; otherwise
  ask in plain text and end the turn.
- `stop(reason)`: end the turn with the reason and the board updated.

Paths: `<enjinia>` is `${CLAUDE_PLUGIN_ROOT}`. The model checker is
`${CLAUDE_PLUGIN_ROOT}/core/scripts/tlc`; trace-check is
`python3 ${CLAUDE_PLUGIN_ROOT}/core/scripts/trace_check.py`.
