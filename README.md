<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/enjinia-logo-dark.svg">
    <img alt="Enjinia" src="assets/enjinia-logo.svg" height="80">
  </picture>
</p>

<p align="center">An engineering lifecycle for agent teams.</p>

Enjinia is a Claude Code plugin that runs a software engineering workflow
like a senior engineer. A team of agents takes a ticket through
requirements, conceptual design, application design, implementation and
review. Each stage ends at a gate: a check
that must pass, and a human approval where your autonomy level asks for
one. Each stage leaves its evidence in files. You own the decisions that
matter and can delegate the rest.

## Example

In Claude Code, inside the repo you want to change:

```
/enjinia:lifecycle Retry failed webhook deliveries with backoff
```

Enjinia sizes the work, then asks you questions until the requirements are
stable. It writes each stage's output to a feature folder in your repo:

```
docs/specs/webhook-retry/
  triage.md         size, mode, domain packs, autonomy level
  as-is.md          existing code only: the current design of what the change touches
  requirements.md   requirements with IDs (BR-1, FR-2, NFR-1)
  concept.md        the model and its invariants (INV-1), with a TLA+ check
  design.md         components, flows and slices
  adr/001-*.md      decision records; a decision an agent made is tagged auto
  tasks.yaml        the task plan: tasks with depends_on, run in dependency order
  review.md         gate results with evidence
```

Every test names the requirements it covers. At each gate, a script
(`core/scripts/trace_check.py`) checks that each requirement traces to an
invariant, a component, a task and a passing test.

## The lifecycle

| Stage | Output | What happens |
|---|---|---|
| 0 Triage | `triage.md` | Size, new or existing codebase, domain packs, autonomy level |
| 1 Requirements | `requirements.md` | An interview, at most 4 questions per round, with no design in it |
| 2 Concept | `concept.md` | Invariants; those about concurrency, crashes, money or data integrity are model checked |
| 3 Application design | `design.md`, `tasks.yaml` | Components, decision records, design review; tests written from the requirements before any code |
| 4 Implementation | commits | One fresh agent per task makes the tests pass; a peer reviewer checks each slice |
| 5 Review | `review.md` | Full test run, traceability check, review through 8 lenses |

A slice is a thin feature increment that works end to end. Stages 2 to 5
repeat for each slice. In an existing codebase, Enjinia first reads the code
the change can affect and writes its current design to `as-is.md`.

Model checking uses [TLA+](https://lamport.azurewebsites.net/tla/tla.html):
a small model of the design, and a tool that tries every order of events to
find one that breaks an invariant.

## Autonomy

You pick a level per run. A decision an agent makes for you is recorded as
an ADR tagged `auto`, and each stage report lists them, so you can overrule
one later.

| Level | You approve | Agents decide and record |
|---|---|---|
| L1 | every stage gate and the task plan | only how to do each task |
| L2 | requirements and concept | design, task plan, slice reviews |
| L3 | requirements and the final review | everything in between |

Some events stop the run at every level, L3 included. Enjinia asks you when
a requirement or invariant would change, when a review reaches 3 rounds,
when cost passes twice the estimate, and before any push, merge or deploy.

## Domain packs

A pack adds questions, checks and review lenses for one domain. Triage picks
the packs that apply.

- `backend`, `frontend-ux`, `data`, `ml-ds`, `ai-engineering`
- `database`: schemas, queries and migrations in an application
- `database-systems`: building a database engine itself

## Install

```
claude plugin marketplace add prvithani/enjinia
claude plugin install enjinia@enjinia
```

Optional tools:
- Python 3 with PyYAML, for the traceability check.
- Java and `tla2tools.jar`, for model checking. Put the jar at
  `~/.local/share/tla/tla2tools.jar` or set `ENJINIA_TLA_JAR`. Without it,
  Enjinia checks those invariants with property tests instead (tests over
  many generated inputs). It marks them `degraded` and says so in the stage
  report.

## Layout

```
core/                  stages, roles, templates, packs, principles, scripts
adapters/claude-code/  the plugin's skills; maps Enjinia to Claude Code tools
docs/specs/enjinia/    the specification and its decision history
```

Nothing in `core/` depends on Claude Code. To run Enjinia in another agent
tool, write a new folder under `adapters/`. The design is in
[`docs/specs/enjinia/spec.md`](docs/specs/enjinia/spec.md).

## Status

Experimental. The Claude Code plugin is built and has run on real tickets.
File formats may still change. A standalone app on the Claude Agent SDK is
planned.

## License

[Apache-2.0](LICENSE).
