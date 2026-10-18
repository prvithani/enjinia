# Lifecycle

The authoritative design is `docs/specs/enjinia/spec.md`. This file is the
runbook the lead (the agent that talks to the human) follows.

## Operations

Stage files use five abstract operations. The adapter maps them to tools.

- `spawn(role, brief)`: start a fresh agent with the role file and a brief of
  file pointers. Never pass a transcript.
- `message(agent, text)`: continue an agent that is still running.
- `run_layer(tasks)`: run independent tasks in parallel.
- `gate(question)`: ask the human and wait.
- `stop(reason)`: end the run and say why.

## Feature folder

Every artifact of one feature lives in one folder, `<feature-dir>`. Default:
`docs/specs/<feature>/` in the target repo. Triage may choose another folder
(for example an ignored scratch folder when another session owns the
branch); it records the choice in `triage.md`.

## Order

0. `stages/triage.md`
1. `stages/as-is.md` (existing mode only; may run beside step 2)
2. `stages/requirements.md`
3. `stages/concept.md` (calls `stages/spike.md` when a fact must be measured)
4. `stages/app-design.md` (stage 3)
5. `stages/implement.md` (stage 4), slice by slice
6. `stages/phase-review.md` (stage 5), per slice and at the end

## Autonomy

Triage proposes a level; the human confirms it at the requirements gate.

| Level | Human approves | Lead decides and logs as an `auto` ADR |
|---|---|---|
| L1 | every gate | nothing |
| L2 (default) | requirements, concept | design, plan, slice reviews |
| L3 | requirements, final review | everything between |

Always `stop` and ask, at every level, when:
- a requirement or invariant would change;
- the model checker finds a violation that no design change fixes;
- a review loop reaches 3 rounds;
- cost or time passes twice the estimate;
- the next step is a push, merge, deploy, or any write outside
  `<feature-dir>` other than a tracker status.

## Rules for every stage

- Evidence or label. Every claim about the code cites file:line, or is marked
  `hypothesis` with how to disprove it.
- Never edit the target repo's code before stage 4.
- Each stage ends by running
  `python3 <enjinia>/core/scripts/trace_check.py <feature-dir> --stage N`
  and reporting the gaps it owns. A gap the stage cannot close is listed in
  the stage report, not hidden.
- Board: one item per stage, with the feature label, in the session board.
