# Claude Code adapter

Maps Enjinia's abstract operations to Claude Code tools.

| Operation | Claude Code |
|---|---|
| `spawn(role, brief, model)` | Agent tool, one fresh subagent per role run |
| `message(agent)` | SendMessage to a running subagent |
| `run_layer(tasks)` | Workflow tool, one parallel layer of `tasks.yaml` |
| `gate(question)` | AskUserQuestion |
| `stop(reason)` | end the turn with the reason |

Skills live in `skills/`, agents in `agents/`. The repo root is the plugin
root, so skills reach shared files as `${CLAUDE_PLUGIN_ROOT}/core/...`.

## Develop

Install once, from the repo root:

    claude plugin marketplace add --scope local "$PWD"
    claude plugin install --scope local enjinia@enjinia

The install is a copy of the working tree, versioned by the HEAD commit.
`claude plugin update --scope local enjinia@enjinia` refreshes it only when HEAD
has changed; then run `/reload-plugins`. To try uncommitted
edits, start a session with `claude --plugin-dir "$PWD"`, which loads in
place.
