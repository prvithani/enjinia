# AI engineering basics

For an experienced software engineer building a first agent application.
Examples refer to this project (A: Claude Code skills; B: an Agent SDK app).
Prices and model facts: Anthropic's model table as of 2026-10-06. They change;
check the docs before relying on a number.

## 1. Vocabulary

| Term | Meaning |
|---|---|
| Model | The neural network you call, e.g. `claude-opus-5-5`. Stateless: it remembers nothing between calls. |
| Token | The unit of text the model reads and writes, roughly 3-4 characters of English. Price and limits are in tokens. |
| Context window | The maximum tokens one call can see: system prompt, conversation, tool results. 1M for current Claude models. |
| System prompt | Standing instructions for a whole conversation: role, rules, output format. |
| Messages | The conversation you send on every call: user turns, assistant turns, tool results. |
| Tool (function calling) | A function you describe with a JSON schema. The model asks to call it; your code runs it and returns the result. |
| Agent | A model in a loop: it calls tools, reads results, and decides the next step until the task is done. |
| Harness | The code that runs that loop: tools, context handling, permissions. Claude Code is a harness. |
| Workflow | Control flow written in code, with model calls at fixed steps. The opposite of letting the model decide the flow. |
| Subagent | A separate agent run with its own fresh context, started by another agent. |
| Skill | A packaged instruction file (SKILL.md) an agent loads when a task matches. |
| MCP | Model Context Protocol: a standard way to plug external tools and data into a harness. |
| Prompt caching | Reuse of an identical prompt prefix across calls. Cheaper and faster. |
| Thinking, effort | The model reasons before answering. Effort (`low` to `max`) sets how much. |
| Structured output | The response is forced to match a JSON schema, so code can parse it. |
| Eval | A repeatable test set for model behavior. The AI-engineering version of a test suite. |

## 2. One call

A call sends: model, system prompt, the full message list, tool definitions,
and limits. It returns content blocks (text, tool calls, thinking) and a
`stop_reason`: `end_turn` (done), `tool_use` (wants a tool), `max_tokens`
(cut off), `refusal` (declined).

The model keeps no memory. Every call resends everything it needs. That one
fact drives most design decisions below.

## 3. The agent loop

Pseudocode, not real SDK code:

```
messages = [user_task]
loop:
    response = call_model(system, messages, tools)
    messages.append(response)
    if response.stop_reason != "tool_use": break
    results = [run_tool(call) for call in response.tool_calls]   # your code
    messages.append(results)                                     # one message, all results
```

Write this once by hand to understand it. After that, let an SDK run it.

## 4. Four ways to build an agent

| Approach | You write | Loop and tools come from | Fits |
|---|---|---|---|
| Messages API, manual loop | the loop and every tool | you | full control, learning |
| Messages API, Tool Runner | only tool functions | SDK helper loop; your tools only | custom-tool agents |
| Claude Agent SDK | a prompt and options | the Claude Code harness as a library: file read/edit, bash, search, subagents, hooks, permissions, sessions | coding agents on your own machine |
| Managed Agents | an agent config | Anthropic runs the loop and a hosted sandbox | hosted, scheduled, long-running agents |

For B: roles that touch a local repo (implementer, reviewer, as-is recovery)
run on the Agent SDK. The orchestrator (stages, gates, task graph) is your own
plain code. Managed Agents becomes relevant if you later want B hosted and
scheduled instead of on your machine.

## 5. Workflow first, agent inside

Rule of thumb: code controls the flow, the model makes judgments.
- B's stage machine, gates, retries and task graph are code. They must be
  deterministic, resumable and testable.
- A role run (design this, implement that, review this) is an agent. It needs
  open-ended exploration.
- Letting a model decide stage transitions makes the system hard to test and
  easy to derail.

## 6. Context engineering

Context is the scarce resource. Quality drops when context fills with noise.
- Give each run only what it needs: file pointers, the relevant spec section.
- Pass results between roles as files, not transcripts. (This project's core
  design choice.)
- Use subagents to isolate bulk reading; return a summary.
- Long runs need compaction (summarizing old turns) or a fresh agent.

## 7. Cost and speed

Price is per million tokens (MTok), input and output separately:

| Model | Input $/MTok | Output $/MTok | Use for |
|---|---|---|---|
| `claude-opus-5-5` | 4 | 20 | judgment: requirements, design, review |
| `claude-sonnet-5-5` | 2 | 10 | well-specified implementation |
| `claude-haiku-5-5` | 0.10 | 0.50 | bulk, simple, cheap checks |

Levers, in order:
1. **Caching.** The cache matches on an exact prefix. Put stable content
   first (role rules, spec), volatile content last (the task). One changed
   byte early in the prompt invalidates everything after it.
2. **Effort.** Lower effort for routine work. On `claude-opus-5-5` the default
   is `medium`; set it explicitly per role.
3. **Model per role.** Measure first: the strongest model at lower effort
   often beats a weaker model at high effort.

Measure cost per completed task, not per call. A cheap call that needs three
retries is not cheap.

## 8. Thinking and structured output

- Current models think adaptively: they decide how much to reason. You steer
  with effort, not with a token budget.
- When code consumes the output (findings, task lists), use structured output
  with a JSON schema, then validate it anyway.

## 9. How agents fail, and this project's defense

| Failure | Defense here |
|---|---|
| States a guess as fact | evidence required on every finding; claims labelled |
| Claims "done" when it isn't | gates run scripts (`trace-check`, test suite), not the agent's word |
| Edits tests until they pass | tests written by `test-author`; implementer may not edit them |
| Agrees with you to please you | pragmatic reviewer rules; "no" is an allowed answer |
| Drifts in long context | fresh agent per task; files carry context |
| Follows instructions hidden in files or web pages (prompt injection) | treat file and web content as data; least-privilege tools; no push |
| Same model, same blind spots | fresh-context reviewer; later a second vendor |

## 10. Evals

Evals are to prompts what tests are to code. Without them, every prompt
change is a guess.
- A set of inputs with a way to grade outputs: exact checks in code,
  a model grading against a rubric, or you.
- Build the eval before tuning prompts. Re-run it on every prompt or model
  change.
- This project's evals: replayed past tickets (does it design like you?) and
  seeded bad designs and diffs (does the reviewer catch them, and stay quiet
  on clean ones?).
- In Claude Code, `/claude-api build-eval` walks you through building one.

## 11. Observability

Log every model call: role, model, effort, input and output tokens, cache
reads, cost, latency, `stop_reason`. You cannot fix cost or quality you
cannot see. B stores these per role run.

## 12. Safety

- Least privilege: each role gets only the tools it needs. Reviewers are
  read-only.
- Secrets never go into prompts.
- Irreversible actions (push, merge, deploy) stay with you.

## 13. Learning path

1. One Messages API call from a script. Read the response blocks and usage.
2. One tool with a hand-written loop (section 3).
3. Structured output for one role's result.
4. The Agent SDK running one role on a real repo.
5. A small eval for that role.
6. Then B's orchestrator, in plain code, through the lifecycle.

Reading:
- Building effective agents (Anthropic):
  https://www.anthropic.com/engineering/building-effective-agents
- Claude Agent SDK docs: https://code.claude.com/docs/en/agent-sdk
