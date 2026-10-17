# Enjinia: decision history

History, in the order decisions were made (2026-10-17). `spec.md` is
authoritative; where this file differs, `spec.md` wins. Notes marked
**Superseded** or **Resolved** point to what replaced an item.

Decided in conversation, not in a round below:
- Existing-codebase mode: one lifecycle for new and existing code
  (`spec.md` 4.2, 4.3, 4.9).
- `spec-to-ship` (a dotfiles skill, never used) is retired; Enjinia
  replaces it.
- The project moved from dotfiles to its own repo.

# Round 1: review of the proposed lifecycle

## What is strong

- The split between conceptual design (what is possible) and application design
  (how to make it possible) is correct. It is the step most AI workflows skip.
  They go from a ticket straight to a component plan.
- Loopbacks to requirements are explicit. Most workflows treat requirements as
  frozen input.
- A task DAG in topological order, with parallel lanes for independent tasks,
  is the right execution model.
- A final review for conceptual integrity and requirement coverage is a real
  gate, not a formality.

## Problems and gaps

1. **Stage versus increment.** Stages 1-3 read as sequential, once per project.
   The bullet "each phase gives a complete, usable flow" asks for increments.
   These conflict unless stages 2-3 run again for each increment.
   Proposal: do stage 1 and a skeleton of stage 2 for the whole project. Then
   run stages 2-5 per vertical slice. This is the spiral model, not waterfall.
   **Resolved:** accepted in round 2.

2. **Formal methods everywhere is too heavy.** Tier by risk, with a trigger:
   - Tier F (formal): state machines, concurrency, money, data integrity.
     TLA+ or Alloy model, model-checked invariants.
   - Tier P (property): pure logic with invariants. Property tests plus a toy
     simulation.
   - Tier E (example): everything else. Examples written as acceptance tests.
   The concept agent proposes a tier per invariant. You approve it at the gate.

3. **Benchmarks at the concept stage mostly cannot run.** No code exists yet.
   Stage 2 can model-check, and it can estimate capacity (queueing model,
   big-O, back-of-envelope). Real latency and throughput need a spike, or they
   move to stage 4 as a measured acceptance test. Label stage 2 numbers as
   estimates.
   **Superseded** by round 2: the spike is a tool of stages 2 and 3.

4. **"Back and forth until both agree" has no stop condition.** Cap it at 3
   rounds, then escalate to you with both positions. Also, agreement between
   two agents on the same model with the same context is weak evidence.
   Errors correlate. The reviewer gets a fresh context: spec, invariants and
   diff only, not the implementer's reasoning. Use a different model for at
   least one review pass.
   **Superseded in part** by round 6: Claude only at first; a second vendor
   reviews only when the eval shows it pays.

5. **Missing spine: a traceability matrix.** Stage 5 "requirement coverage"
   is not checkable without it. One table:
   `requirement -> invariant -> component -> task -> test -> evidence`.
   Each stage fills its column. A gate fails if a row has an empty column that
   the stage owns. A loopback uses it for impact analysis: change R3, and the
   matrix lists the affected tasks and tests.

6. **Missing: a decision log (ADRs).** Each design decision with its options,
   choice and reason. Without it, later agents and loopbacks re-argue settled
   decisions.

7. **Missing: oracle independence.** The tests that verify a task must come
   from the spec, not from the implementer. Acceptance and property tests are
   written in stage 3 or at the start of stage 4 by an agent other than the
   implementer. Otherwise the implementer writes tests that pass its own bugs.

8. **Missing: entry triage.** A one-line fix should not run five stages.
   Size the work at entry (small / medium / large) and pick which stages run.
   Without this, the cost of the full flow lands on every task.

9. **"Known efforts and estimations" is optimistic for agents.** Token and
   time estimates from agents are unreliable. Use size buckets, record
   actuals on the board, and calibrate later.

10. **"Imitates me" needs an eval, not only a prompt.** The process imitates
    a senior engineer's workflow. Your judgment is a separate thing. Encode it
    from what you already wrote (CLAUDE.md constraints, branch-review lenses,
    mechanism vs policy). Then test it: replay 3-5 past tickets you designed,
    and compare the agent's stage-2 and stage-3 output with what you shipped.
    That is the only way to know whether it imitates you.

## Context and cost

- **Artifacts carry context, agents do not.** Each stage writes a compact
  file. Agents read files, not transcripts.
- **Implementers are fresh per task.** Each gets a file-pointer brief:
  task card, interface section, invariants, test list. No full-context forks.
- **Reviewers persist per stage.** The same reviewer agent re-checks after
  fixes over SendMessage. That is the branch-review pattern you already use.
- **Stable prompt prefix.** All task agents read the same spec files first.
  That helps prompt caching.
- **Model per role.** Opus for requirements, concept, design and review.
  A smaller model for well-specified tasks.

## Mechanism and policy

The lifecycle is policy. The mechanism already exists in Claude Code: skills,
subagents, SendMessage, Workflow `pipeline`/`parallel` for the DAG, hooks for
gates, `board.md` and Linear for tracking. Build the policy on top of it.
**Superseded in part** by round 5: gates run as scripts, not harness hooks.
A second lifecycle (for example a bug-fix flow) then reuses the same
mechanism.

"Graph engineering" here means a `depends_on` field per task and a
topological sort. The Workflow tool runs the layers. No graph engine needed.

## Human gates

**Superseded** by the autonomy levels in round 2.

| Gate | Automatable later? |
|---|---|
| Requirements sign-off | Never |
| Concept sign-off (invariants, verification tier) | Never |
| Application design sign-off | Never |
| Task plan approval | Maybe, for small work |
| Per-slice phase review | Yes, after the eval shows it is reliable |
| Final review, commit, push | Never (git-guard) |

## Build options

**Resolved:** option C (round 2). `spec-to-ship` was later retired, so
Enjinia is built as its own plugin, not as an extension of it.

- **A. Claude Code skills and agents (recommended).** Extend `spec-to-ship`
  into stage skills: `requirements`, `concept`, `app-design`, `task-plan`,
  `implement`, `phase-review`. `branch-review` becomes the phase gate.
  Artifacts in `docs/specs/<feature>/`. Cheapest, and it reuses all of
  your tools.
- **B. Standalone app on the Agent SDK.** Own orchestrator, persistence and
  UI. Justified only for multi-user or non-Claude-Code use.
- **C. A now, B when a specific limit of A appears.**

Suggested order if you choose A: build `requirements` and `concept` first.
They are the stages that are new. Stages 4-5 are mostly in `spec-to-ship` and
`branch-review` already. Dogfood each stage on one real ticket before you
build the next.

## Open questions

**Resolved:** 1 yes (round 2); 2 own tooling first, then an application (B);
3 Linear as record, board for live status (round 2).

1. Stage versus increment: is the per-slice spiral (problem 1) what you mean?
2. Scope: your own Claude Code tooling, or a product or service for others?
3. Tracker: `board.md`, Linear, or both (board for the session, Linear as
   record)?

---

# Round 2: decisions and proposals

## Decided
- Problems 1, 2, 4 and 6: accepted. Per-slice spiral; verification tier by risk.
- Build approach: C. Claude Code skills now; Agent SDK app is the goal.

## Accepted: POC placement (problem 3)
A spike is a tool that stages 2 and 3 call, not a separate stage.
- Trigger: a decision depends on a number or a capability that cannot be
  looked up. Example: "does SKIP LOCKED hold 2,000/s on our primary?"
- Output: a measurement and an ADR. The code is thrown away, time-boxed.
- Stage 2 calls it for feasibility ("can this concept work at all?").
  Stage 3 calls it to choose between designs ("which option meets NFR-1?").
- Full NFR benchmarks stay in implementation as acceptance tests. The first
  slice is a walking skeleton: thin, end to end, and it stays.
- Why not a mandatory stage: most work has no measurable unknown. A fixed
  stage adds its cost to every ticket.

## Accepted: traceability matrix (problem 5)
Don't maintain the matrix by hand. Derive it.
- IDs live in the source artifacts: requirements.md (`BR-2`), concept.md
  (`INV-1 covers BR-2`), tasks.yaml (`covers: [BR-2]`), tests (in Clojure,
  `deftest` metadata such as `^{:covers [:BR-2]}`).
- A small script builds the matrix from these files and the test report, and
  fails on gaps: a requirement with no task or test, a task that covers
  nothing, a test ID that doesn't exist, an invariant without a test at its
  tier.
- Gates and the final review run the script. One source per fact (DRY); the
  matrix is a view.

## Accepted: tracker split
- Linear: the ticket and its record. Optionally one sub-issue per slice if
  the team needs to see it. Updated at gates: spec link, slice done.
- tasks.yaml (in docs/specs/<feature>/): task structure. depends_on, covers,
  size. The Workflow reads it.
- board.md: task status during work. Labels match tasks.yaml.
- Caveat: the session board ends with the session. A multi-session ticket
  needs its items on the project board (promotion rule), or status stored in
  tasks.yaml. For B, a real store replaces both.

## Accepted: autonomy levels
Gate by reversibility and blast radius, not by stage. Triage proposes a
level; you confirm it at the requirements gate.

| Level | You approve | Agent decides and logs |
|---|---|---|
| L1 supervised | every stage gate, task plan | nothing beyond a task |
| L2 default | requirements, concept | design, plan, slice reviews |
| L3 trusted | requirements, final | everything in between |

Always stop, at every level:
- a requirement or invariant would change (loopback that changes scope)
- the model checker finds a violation with no design fix
- a review loop reaches 3 rounds
- cost or time exceeds the estimate by 2x
- push, merge, deploy, or any external write except Linear status

Each auto decision goes into the decision log tagged `auto`. The stage report
lists them, so you can veto after the fact.

Conflict: your CLAUDE.md says design forks always wait. The lifecycle skill
would need a scoped exception: at L2 and above, forks inside the approved
concept are decided and logged.

## Accepted: pragmatic reviewer (branch-review and lifecycle reviewers)

The last rule (verified or suspected) was dropped: `branch-review` already
requires a repro or measurement for every finding.
Replace "Not finding anything is also fine." with:
- Report a finding only with one of: a concrete failure (input or state, then
  wrong result), a measured cost, or a broken rule from CLAUDE.md or the spec.
  "Could be cleaner" alone is not a finding.
- Zero findings is a normal result for a clean diff. The number of findings
  does not measure review quality.
- Critical or Important only if a senior engineer would block the merge.
- At most 3 Nits per lens, and only if they change meaning or mislead.
  Code that follows the codebase convention is not a Nit.
- Don't reopen a decision recorded in the spec or an ADR without new evidence.
- Mark each finding verified (repro ran) or suspected. A suspected finding is
  never Critical.

---

# Round 3: making the designer follow design principles

Status: accepted.

Models already know the principles. They fail at applying them to one design.
A prompt that lists principles adds little. Make the principles checkable.

## 1. Principles as checks, not slogans

One reference file, `design-principles.md` (in `core/`, per round 5). Each principle becomes a
question with an observable answer in `design.md`.

| Principle | Check on the design |
|---|---|
| Separation of concerns, single responsibility | Each component states one responsibility in one sentence, one kind of work (UI / domain / persistence / infra). |
| Encapsulation | Each component lists what it exposes. No other component references anything outside that list. |
| Loose coupling, dependency direction | `depends_on` per component. No cycles. Domain never depends on infra. |
| DRY (knowledge) | Each data entity has exactly one owning component. |
| YAGNI | Each component and extension point realizes at least one requirement or invariant. |
| Mechanism vs policy | For each generic component: "if a second user appeared, would I refactor?" Answer recorded. |
| Illegal states unrepresentable | Each invariant names where it is enforced: type, constraint, or runtime check. |

Source: your CLAUDE.md "Timeless constraints", made operational. Additions,
only if you want them: deep modules (small interface, much behind it) and
bounded contexts (one word, one meaning per context).

## 2. A design template that exposes the answers

`design.md` gets fixed fields per component: responsibility, owns (data),
exposes, depends_on, realizes (requirement and invariant IDs). The designer
cannot skip a principle silently, because an empty field is visible.

## 3. Machine checks where the structure allows

The rows for dependency direction, DRY and YAGNI are graph and set checks.
`trace-check` already parses IDs and builds a task graph. The same graph code
checks the component graph: cycles, layer rule, single owner, no component
without a requirement. One graph mechanism, two policies (tasks, components).

## 4. Judgment checks by an independent reviewer

The rest (one responsibility, mechanism vs policy, interface size) need
judgment. A fresh reviewer applies `branch-review` lens 8 (Design) to
`design.md` before any code exists. Pragmatic rules apply. One pass on a
different model.

## 5. Options before choice

Each significant decision has an ADR with 2-3 options and tradeoffs. When two
principles conflict, the ADR names which one won and why, by your rule:
"pick the one that cuts future cost in this codebase."

## 6. Calibrate the reviewer

Seed 3-5 deliberately bad designs: a cycle, a god component, a speculative
extension point, two owners of one entity, policy inside a mechanism. The
reviewer must catch each. Also run it on one good design and expect zero
findings. This measures both misses and noise.

## Open point

Still open (`spec.md` 15). Unverified: whether subagents receive the global CLAUDE.md. If they do not,
the reviewer brief must include `design-principles.md` explicitly. Check in P3.

---

# Round 4: design patterns and implementers

Status: accepted; in plan P2-P4.

Yes, with one split: who chooses a pattern depends on its scale.

| Scale | Examples | Chosen by | Implementer's role |
|---|---|---|---|
| Architectural | outbox, saga, event sourcing | concept / app design | follows |
| Component | state machine, strategy, adapter, registry | app design, `pattern:` field per component with a reason | follows |
| Code idiom | guard clause, data-driven dispatch, early return | implementer | chooses freely |
| House pattern | how this codebase does errors, config, state, tests | already in the code | follows |

Why implementers don't pick component patterns:
- Pattern choice is a design decision. Chosen per task, it gives a different
  pattern for the same problem in two tasks.
- A pattern added without need is the most common over-engineering, for
  example an interface with one implementation.
- Many GoF patterns are a function, a map or a multimethod in Clojure. The
  catalog must be language-aware.

Mechanism:
- `patterns.md` reference, language-aware: when each pattern earns its place,
  and its plain form in the target language.
- As-is recovery writes the house patterns to
  `docs/architecture/conventions.md` in the target repo. The implementer
  brief includes the relevant section.
- An implementer that sees a need for a pattern not in `design.md` stops and
  raises it to the peer reviewer. It does not add it.
- The peer reviewer checks: the named pattern is used; no new pattern or
  named abstraction appears without a design entry.

---

# Round 5: harness independence, and building B with A

Status: accepted.

## 1. Independent of Claude Code without losing quality

Quality comes from three things. Only one of them is harness-specific.

| Source of quality | Portable? |
|---|---|
| Artifacts, IDs, templates, principles, patterns | Yes. Markdown and YAML. |
| Checks (`trace-check`, component graph) | Yes. A CLI any agent can run. |
| Orchestration: fresh-context agents, persistent reviewer, parallel layers, human gates | No. Each harness has its own primitives. |

So split the repo in two layers:
- **core/**: stage instructions, artifact schemas, principles, patterns,
  scripts. No harness names in it. Skills use the SKILL.md format, which
  other harnesses also read (to verify per harness).
- **adapters/<harness>/**: maps a short list of abstract operations to native
  tools. Operations: `spawn(role, brief, model)`, `message(agent)`,
  `run_layer(tasks)`, `gate(question)`, `stop(reason)`. Claude Code: Agent,
  SendMessage, Workflow, AskUserQuestion.

This is how superpowers (Codex, Pi, Hermes reference files) and pstack (a
generated Claude Code tree from a Cursor source) handle it.

Keeping quality:
- Gates live in scripts, not in harness hooks, so every harness runs the same
  checks.
- When a harness lacks a primitive, degrade loudly. Example: no subagents
  means the reviewer runs in a separate CLI session, not in the same context.
  If even that is impossible, the review is marked `degraded` in review.md.
- Prove it: the P6 eval (replayed tickets) and the seeded bad designs run on
  each adapter. An adapter ships only if its scores match the Claude Code
  baseline.

YAGNI: build only the Claude Code adapter now. Keep the seam (no harness
names in core). B is the second adapter, so the seam has a real second user.

**Resolved** by round 6. Open question: harness independence only, or model independence too? The
Claude Agent SDK runs Claude models only. Multi-model (as pstack does) needs
a model-agnostic layer in B.

## 2. Build B with A

Yes. B is a strong first real project for A:
- It is greenfield and large: it runs the full lifecycle.
- Its core is a state machine (stages, gates, resume after crash, idempotent
  steps). That is formal-tier work in stage 2.
- B becomes the second adapter, which proves the core/adapter seam.

Conditions:
- A must exist through P4 and pass calibration first. Otherwise a failure
  could come from A or from B, and you can't tell which.
- Feed A's failures from dogfooding and P6 into B's requirements. Otherwise
  B copies A's flaws.
- Keep the artifact formats identical, so a spec started in A can finish in B.

What B adds over A: stage machine in code instead of in a prompt, durable
state instead of files and boards, resume after crash, scheduling, cost
tracking, multi-user, a UI.

Order: A P0-P4, then A stages 1-3 on B while P5-P6 finish, then implement B
with A.

---

# Round 6: a model-neutral layer

Status: accepted. Claude only at first; the `run_role` seam makes a second
vendor additive. Second-reviewer guide: `dual-reviewer.md`.

## Short answer

Yes, if the seam sits at the role, not at the API call or the agent loop.

## Where the cost of neutrality comes from

| Seam | Quality and performance cost |
|---|---|
| API call (one chat interface for all vendors) | High. Lowest common denominator. Vendors differ in prompt caching, reasoning blocks across tool calls, tool-call formats, structured output, context size, server-side tools. Abstracting them away loses cache hits (cost, latency) and reasoning continuity. |
| Agent loop (own harness for all models) | Highest. You rebuild what each vendor's harness already tunes: tools, context compaction, subagents, permissions. Prompts tuned for one model also behave differently on another. |
| Role (brief and files in, artifact and status out) | Low. Each role runs on its vendor's own harness (Claude Agent SDK, or another vendor's CLI or SDK). The orchestrator only sees files. |

The lifecycle already passes context through files, not transcripts. So the
role boundary exists already; it costs almost nothing to make it the seam.

## Mechanism and policy

- Mechanism: `run_role(role, brief, files, budget) -> artifact, status, cost`.
  One runner per vendor. Each runner declares its capabilities (resume a
  session, parallel tools, caching), and the orchestrator uses them only when
  present.
- Policy: which model runs which role. Decided by the eval, not by taste.

## What it does not fix

- Quality is per (prompt, model) pair. A role prompt tuned on Claude needs
  its own eval on another model, and may need a variant.
- Prompt cache is per vendor. Roles on different vendors share no cache.
  This is small: roles already start from files, not from a shared transcript.
- Process cost: one subprocess or SDK session per role run. Small next to
  model latency.
- Data: each extra vendor receives the code it reviews. Fine for this
  personal project; check before pointing it at an employer's repo.

## Where multiple models pay off

The clearest gain is an uncorrelated reviewer: a second model catches what
the first one consistently misses. That is a single role swap.

## Recommendation

- B v1: Claude only, but every role goes through `run_role`.
- Add a second vendor for the reviewer role only, when the seeded-bad-design
  eval shows it catches defects Claude misses.
- Add more roles only on eval evidence.

---

# Round 7: specializations

Status: accepted; packs in plan.

## Specializations

The stages hold for every domain. What differs per domain is the content of
each stage. So: one generic lifecycle (mechanism) plus domain packs (policy)
that fill named slots.

Rule for a separate pack: its slot contents differ from every other pack, or
more than one pack needs them (then a separate pack keeps one copy).

One row per pack. Every pack fills the same slots. Review lenses are added to
the 8 `branch-review` lenses.

| Pack | Extra requirements | Concept artifact | Spike | Verification | Review lenses | Patterns | Role variant |
|---|---|---|---|---|---|---|---|
| backend (default) | latency, throughput | invariants, state model | measurement | formal, property, example tiers | concurrency, API contract compatibility, idempotent retries | `principles.md`, `patterns.md` | implementer |
| ai-engineering | behavior spec with quality bar, cost and latency per task, failure policy | workflow or agent per step, roles and context, tool surface, failure defenses | prompt prototype on 5-10 real examples | evals (code, model-rubric, human graders), regression eval per prompt or model change, cost and latency, prompt-injection cases | context hygiene, cache-friendly prompt order, least-privilege tools, validated structured output, deterministic orchestrator, eval coverage per role | prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, role runner | eval-author |
| database | access patterns, volume and growth, retention | logical and physical model, keys, constraints for invariants, indexes from access patterns | query plan on realistic volume, migration rehearsal on a copy | EXPLAIN plans, timed migration dry run, lock analysis, load test, constraint tests | online-migration safety, index use, invariants in constraints, reversible migrations | normalization, migration patterns | implementer with a scratch database |
| data | freshness, completeness | data model, lineage, data contracts | dry run on sample data | data tests, reconciliation, backfill dry run | lineage, idempotent backfills, cost per run | dimensional modeling | implementer with a warehouse connection |
| frontend-ux | user flows, accessibility | information architecture, UI state chart, interaction model | clickable prototype | visual regression, accessibility audit, interaction tests | accessibility, design-system use, visual consistency | component and state patterns | implementer with a browser tool |
| database-systems | workload mix, isolation level, durability guarantee, protocol compatibility | storage model, concurrency control, recovery, replication; formal tier by default | microbenchmark, I/O cost model | model checking, deterministic simulation, fault injection, history checking, SQL fuzzing, differential tests, standard benchmarks | crash consistency of every write path, on-disk format compatibility, latch and lock ordering, benchmark regression gate | WAL, MVCC, LSM compaction, buffer pool, group commit | implementer with a simulation harness; fault-injection tester |
| ml-ds | metric target, baseline | problem framing, metric, baseline, data and labels | experiment | eval set, holdout metrics, leakage checks | leakage, eval contamination, reproducibility | experiment design | experimenter |

Pack scopes:
- ai-engineering: building LLM and agent applications. B is one, and so are
  A's own skills. ml-ds trains models.
- database: schema, SQL and migrations inside an application. Backend and
  data both use it.
- database-systems: building a database engine. The best fit for the
  lifecycle: formal specs of transactions and replication are common practice
  there, and correctness under crashes is the core requirement.

Cross-domain features: a feature often spans frontend, backend and database.
Each component in `design.md` gets a `domain:` field. Its tasks then get that
pack's checks and lenses. One feature, several packs, one lifecycle.

Where the fit is weaker:
- ML and exploratory data science are experiment-driven. Requirements
  sharpen from results. The spiral handles it only if the experiment loop is
  first-class: walking skeleton = a dumb baseline end to end, then measured
  iterations with a decision log.
- A data-science question with an answer, not code, as deliverable, is an
  investigation: question, method, evidence, answer. Same gates, fewer stages.
- UX research needs real users. Agents can prepare and synthesize; the
  research input comes from you.

Build order follows real work. Define the slots in `core/` as it is built
(cheap: they are where the templates live). Build backend and ai-engineering
first: B is the first real project and is AI engineering, and A's own skills
get evals under that pack. The rest when real work needs them.
