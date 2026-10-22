# Enjinia: specification

Status: approved design. This file is authoritative. `decisions.md` records
how each decision was reached; where they differ, this file wins.

Related: `dual-reviewer.md` (second-vendor reviewer protocol), `demo.html`
(mock run of one feature), `../../guides/ai-engineering-basics.md`.

## 1. Purpose

Enjinia runs a software engineering workflow like a senior engineer:
requirements, conceptual design, application design, implementation and
review, with gates, loopbacks and evidence at each step. A team of agents
does the work. The human owns the decisions that matter and can delegate the
rest.

## 2. Goals and non-goals

Goals:
- Correct before done. Every claim of done is backed by a check that ran.
- One lifecycle for new and existing codebases, and for every domain.
- Each increment delivers a complete, usable flow.
- Context is preserved through files, so agents stay small and cheap.
- Harness and model vendor are replaceable without loss of quality.

Non-goals:
- No graph engine. Tasks carry `depends_on`; a topological sort orders them.
- No new tracker. Linear is the record; boards hold live status.
- No autonomy over irreversible actions (push, merge, deploy).

## 3. Delivery

- **A**: Claude Code plugin (skills, agents, scripts). Built first.
- **B**: standalone application on the Claude Agent SDK. Built with A, as A's
  first real project, after A is calibrated.

A and B share `core/` and the artifact formats, so a spec started in A can
finish in B.

## 4. Lifecycle

### 4.1 Shape

Stage 0 and stage 1 run once per feature. A skeleton of stage 2 covers the
whole feature. Then stages 2-5 repeat for each slice (spiral model). Each
slice is usable on its own. The first slice is a walking skeleton: the
thinnest end-to-end version, and it stays.

A stage may loop back to an earlier stage when it finds a gap. A loopback
that changes a requirement or an invariant always stops for the human.

### 4.2 Stage 0: triage

Sets, for one feature:
- size: small, medium or large. Small work skips stages 2-3 and uses a
  one-paragraph spec.
- mode: new or existing codebase.
- domain packs that apply (section 9).
- proposed autonomy level (section 8). The human confirms it at the
  requirements gate.
- existing mode only: the blast radius (callers, data and contracts the
  change can affect).

### 4.3 As-is recovery (existing mode only)

A read-only agent recovers the current model of the blast radius:
components, enforced invariants, conventions, house patterns, test coverage.
Output: `as-is.md` for the feature, and updates to `docs/architecture/` in
the target repo (including `conventions.md`). Later features start from it.

### 4.4 Stage 1: requirements

An interview, in rounds, until requirement IDs are stable. Requirement types:
`BR-` business, `FR-` functional, `NFR-` non-functional, `TR-` technical,
`G-` goals, `NG-` non-goals, `EB-` existing behavior that must not change
(existing mode). Packs add types.

### 4.5 Stage 2: conceptual design

Pure concepts, no technology choices. Output: the model, invariants
`INV-n` with the requirements each covers, and a verification tier per
invariant:

| Tier | Use for | Check |
|---|---|---|
| formal | state machines, concurrency, money, data integrity | model (TLA+ or Alloy), model checker |
| property | pure logic with invariants | property tests, toy simulation |
| example | everything else | examples as acceptance tests |

Numbers at this stage are estimates (queueing model, big-O) and are labelled
so. In existing mode, the concept is the difference between the as-is model
and the new requirements. If a new requirement breaks an existing invariant,
that part is redesigned from first principles.

### 4.6 Spike

A tool that stages 2 and 3 call, not a stage. Trigger: a decision depends on
a number or a capability that cannot be looked up. Time-boxed. Output: a
measurement and an ADR. The spike code is thrown away. Stage 2 uses spikes
for feasibility; stage 3 uses them to choose between designs.

### 4.7 Stage 3: application design

Output:
- `design.md`: components, interfaces, sequence flows, slices. Fixed fields
  per component (section 7.1).
- ADRs: each significant decision with 2-3 options, the choice and the
  reason. When two principles conflict, the ADR names the winner and why:
  the one that cuts future cost in this codebase.
- `tasks.yaml`: tasks per slice (section 5).
- Tests from the spec, written by `test-author` before implementation.
  Existing mode: characterization tests for touched code that has none.

The design is reviewed before code exists (section 7).

### 4.8 Stage 4: implementation

Per slice, tasks run in topological layers; tasks in one layer run in
parallel. Each task:
- a fresh `implementer` with a file-pointer brief: task card, linked spec
  sections, invariants, test list, relevant `conventions.md` section.
- the implementer may not edit tests written by `test-author`.
- a `peer-reviewer` reviews; at most 3 rounds, then both positions go to the
  human.
- existing mode: refactor the touched code to the principles first, as its
  own reviewable step, then change behavior.

### 4.9 Stage 5: review

Slice review, after each slice: the `branch-review` lenses plus the slice
pack's lenses, a check that the slice is usable on its own, and
`trace-check`.

Final review, after the last slice:
- every traceability row complete.
- every invariant has a test at its tier.
- conceptual integrity: each responsibility lives in its owning component.
- every deviation from `design.md` has an ADR.
- NFR numbers measured, not estimated.
- existing mode: every `EB-` row pinned by a passing test; codebase
  conventions followed.

## 5. Artifacts

Per feature, in the target repo:

```
docs/specs/<feature>/
  triage.md         size, mode, packs, autonomy level, blast radius
  as-is.md          existing mode only
  requirements.md   requirement IDs
  concept.md        model, INV-n with covers and tier, estimates
  design.md         components with fixed fields, flows, slices
  adr/NNN-*.md      decision log; agent decisions tagged `auto`
  tasks.yaml        tasks
  review.md         slice and final review results
docs/architecture/  project-level as-is model and conventions.md
```

`tasks.yaml` entry fields: `id`, `label`, `slice`, `depends_on`, `covers`,
`size` (bucket, not a time estimate), `reads`, `tests`, `done_when`.

Tests carry `covers` metadata. Clojure: `^{:covers [:BR-2]}` on `deftest`.

Formats are provisional until the eval (plan P6). Each format has one reader
in `trace_check.py` and one example in its fixture, so a change touches
those two places. Freeze them before B reads them.

## 6. Traceability

The matrix `requirement -> invariant -> component -> test -> task ->
evidence` is derived, never maintained by hand. `trace-check` builds it from
the artifacts and the test report and fails on:
- a requirement with no task or no test.
- a task that covers nothing.
- a test ID that does not exist.
- an invariant without a test at its tier.
- a cycle in `tasks.yaml`.

The same graph code checks the component graph from `design.md`: no cycles,
domain never depends on infrastructure, one owner per data entity, every
component realizes a requirement or invariant.

A gate fails if a column that the stage owns is empty. Impact analysis of a
changed requirement reads the same matrix.

## 7. Design quality

### 7.1 Principles as checks

Each principle is a question with a visible answer in `design.md`. The
component fields are: responsibility, layer (ui, domain, persistence, infra),
owns, exposes, depends_on, realizes, pattern, domain (the pack). The pack's
`layers.yaml` lists forbidden layer dependencies.

| Principle | Check |
|---|---|
| Separation of concerns, single responsibility | One responsibility in one sentence; one kind of work. |
| Encapsulation | Exposes is listed; no reference outside it. |
| Loose coupling, dependency direction | No cycles; domain does not depend on infra. |
| DRY (knowledge) | One owner per data entity. |
| YAGNI | Each component and extension point realizes a requirement or invariant. |
| Mechanism vs policy | "If a second user appeared, would I refactor?" answered. |
| Illegal states unrepresentable | Each invariant names where it is enforced. |

Structural rows are machine-checked (section 6). Judgment rows are checked by
a fresh-context reviewer with the Design lens.

### 7.2 Patterns by scale

| Scale | Example | Chosen by | Implementer |
|---|---|---|---|
| Architectural | outbox, saga | stages 2-3 | follows |
| Component | state machine, strategy, adapter | stage 3, `pattern:` field with a reason | follows |
| Code idiom | guard clause, data-driven dispatch | implementer | chooses |
| House pattern | errors, config, tests in this codebase | existing code | follows |

`patterns.md` is language-aware: when a pattern earns its place, and its
plain form in the target language. An implementer that needs a pattern not
in `design.md` raises it; it does not add it.

### 7.3 Review rules

Every reviewer, human-facing or internal:
- A finding needs a concrete failure (input or state, then wrong result), a
  measured cost, or a broken rule from the spec or an ADR. "Could be
  cleaner" is not a finding.
- Zero findings is a normal result.
- Critical or Important only if a senior engineer would block the merge.
- At most 3 Nits per lens, only if they change meaning or mislead.
- A settled decision (spec or ADR) is not reopened without new evidence.
- Reviewers get a fresh context: spec sections, invariants and the diff, not
  the implementer's reasoning.
- After fixes, the same reviewer re-checks its own findings.

### 7.4 Reviewer calibration

The design reviewer is tested on 3-5 seeded bad designs (cycle, god
component, speculative extension point, two owners of one entity, policy in
a mechanism) and one good design. It must catch each defect and report zero
findings on the good design.

## 8. Autonomy

Gates are set by reversibility and blast radius, not by stage.

| Level | Human approves | Agent decides and logs |
|---|---|---|
| L1 supervised | every stage gate, task plan | nothing beyond single tasks |
| L2 default | requirements, concept | design, plan, slice reviews |
| L3 trusted | requirements, final review | everything in between |

Always stop, at every level:
- a requirement or invariant would change.
- the model checker finds a violation with no design fix.
- a review loop reaches 3 rounds.
- cost or time exceeds twice the estimate.
- push, merge, deploy, or any external write other than a Linear status.

Every agent decision is an ADR tagged `auto`. Each stage report lists them,
so the human can veto after the fact.

## 9. Domain packs

The lifecycle is the mechanism. A domain pack is policy that fills fixed
slots: extra requirement types, concept artifact, spike kind, verification,
extra review lenses, patterns, role variant. Each component in `design.md`
names its `domain`; its tasks get that pack's checks and lenses.

A pack is separate when its slot contents differ from every other pack, or
more than one pack needs them.

| Pack | Extra requirements | Concept artifact | Spike | Verification | Extra review lenses | Patterns | Role variant |
|---|---|---|---|---|---|---|---|
| backend (default) | latency, throughput | invariants, state model | measurement | formal, property, example tiers | concurrency, API contract compatibility, idempotent retries | `principles.md`, `patterns.md` | implementer |
| ai-engineering | behavior spec with quality bar, cost and latency per task, failure policy | workflow or agent per step, roles and context, tool surface, failure defenses | prompt prototype on 5-10 real examples | evals (code, model-rubric, human graders), regression eval per prompt or model change, cost and latency, prompt-injection cases | context hygiene, cache-friendly prompt order, least-privilege tools, validated structured output, deterministic orchestrator, eval coverage per role | prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, role runner | eval-author |
| database | access patterns, volume and growth, retention | logical and physical model, keys, constraints for invariants, indexes from access patterns | query plan on realistic volume, migration rehearsal on a copy | EXPLAIN plans, timed migration dry run, lock analysis, load test, constraint tests | online-migration safety, index use, invariants in constraints, reversible migrations | normalization, migration patterns | implementer with a scratch database |
| data | freshness, completeness | data model, lineage, data contracts | dry run on sample data | data tests, reconciliation, backfill dry run | lineage, idempotent backfills, cost per run | dimensional modeling | implementer with a warehouse connection |
| frontend-ux | user flows, accessibility | information architecture, UI state chart, interaction model | clickable prototype | visual regression, accessibility audit, interaction tests | accessibility, design-system use, visual consistency | component and state patterns | implementer with a browser tool |
| database-systems | workload mix, isolation level, durability guarantee, protocol compatibility | storage model, concurrency control, recovery, replication; formal tier by default | microbenchmark, I/O cost model | model checking, deterministic simulation, fault injection, history checking, SQL fuzzing, differential tests, standard benchmarks | crash consistency of every write path, on-disk format compatibility, latch and lock ordering, benchmark regression gate | WAL, MVCC, LSM compaction, buffer pool, group commit | implementer with a simulation harness; fault-injection tester |
| ml-ds | metric target, baseline | problem framing, metric, baseline, data and labels | experiment | eval set, holdout metrics, leakage checks | leakage, eval contamination, reproducibility | experiment design | experimenter |

Pack scopes: ai-engineering builds LLM and agent applications; ml-ds trains
models. database is schema, SQL and migrations inside an application;
database-systems builds a database engine.

Variants of the lifecycle shape:
- ml-ds: experiment-driven. The walking skeleton is a simple baseline end to
  end; then measured iterations with a decision log.
- A question whose deliverable is an answer, not code: question, method,
  evidence, answer. Same gates, fewer stages.
- UX research input comes from real users, through the human.

Built first: backend and ai-engineering. Others when real work needs them.

## 10. Roles

A role is data: purpose, inputs it may read, output and its schema, tools
allowed, model and effort, budget, lifetime, rules. Role files live in
`core/roles/`.

| Role | Lifetime | Reads | Writes | Model |
|---|---|---|---|---|
| requirements-analyst | stage 1, across interview rounds | ticket, human answers, logs | requirements.md | opus |
| as-is | per feature, read-only | target codebase | as-is.md, docs/architecture/ | opus |
| concept-modeler | stage 2 | requirements.md, as-is.md | concept.md, models | opus |
| app-architect | stage 3 | requirements, concept, codebase | design.md, ADRs, tasks.yaml | opus |
| test-author | end of stage 3 | requirements, invariants, interfaces | tests | opus |
| implementer | one fresh agent per task | task card and linked sections | code diff | sonnet |
| peer-reviewer | one per slice, persistent | spec sections, diff | review notes | opus |
| gate-reviewer | per slice and final | all artifacts, matrix | review.md | opus |

Packs add role variants (section 9). Models per role are defaults; the eval
decides changes.

## 11. Context and cost

- Files carry context between roles, not transcripts.
- Each role gets only what it needs: file pointers and the relevant
  sections.
- Stable content first in every prompt (role rules, spec), volatile content
  last, for prompt caching.
- Effort is set per role.
- Cost is measured per completed task, not per call. Every model call is
  logged: role, model, effort, tokens, cache reads, cost, latency, stop
  reason.

## 12. Tracking

- Linear: the ticket and its record, updated at gates.
- `tasks.yaml`: task structure.
- Board: live task status, with the same labels as `tasks.yaml`. Items still
  open at the end of a session move to the project board.
- B replaces boards and files with a durable store.

## 13. Architecture

### 13.1 Core and adapters

```
core/                 harness-free: stage instructions, roles, templates,
                      packs, principles, patterns, scripts
adapters/<harness>/   maps abstract operations to one harness's tools
```

Abstract operations: `spawn(role, brief, model)`, `message(agent)`,
`run_layer(tasks)`, `gate(question)`, `stop(reason)`. The Claude Code
adapter maps them to Agent, SendMessage, Workflow and AskUserQuestion.

- No harness names in `core/`.
- Gates run as scripts, so every harness runs the same checks.
- A missing primitive degrades loudly. Example: a harness without subagents
  runs the reviewer in a separate session. If that is impossible, the review
  is marked `degraded`.
- An adapter ships only if it matches the Claude Code baseline on the eval.

### 13.2 Role runner

Every role runs through
`run_role(role, brief, files, budget) -> artifact, status, cost`. One runner
per model vendor; each declares its capabilities (resume, caching, parallel
tools), and the orchestrator uses them only when present. The boundary sits
at the role, not at the API call or the agent loop, so each vendor runs on
its own tuned harness. Which model runs which role is policy, set by the
eval.

Enjinia runs on any codebase. Which vendors may receive a target repo's code
is a per-repo setting; a role never runs on a vendor the repo does not allow.

Claude only at first. A second vendor is added for the reviewer role only,
when the seeded-defect eval shows it catches defects Claude misses. Protocol:
`dual-reviewer.md`.

### 13.3 B

B adds: the stage machine in code instead of in prompts, durable state,
resume after a crash, scheduling, cost tracking, multiple users, a UI. The
orchestrator is deterministic code; only work inside a role is agentic.

Order: A through implementation and review, calibrated. Then A runs stages
1-3 on B while A's eval finishes. Then A implements B. A's failures found in
use become B's requirements.

## 14. Evaluation

- Replay 3-5 past tickets the human designed; compare stage 2-3 output with
  what shipped.
- Seeded defects: bad designs and buggy diffs with known defects, plus clean
  ones that must produce zero findings.
- Run on every prompt, role, model or adapter change.

## 15. Open points

- Whether Claude Code subagents receive the global CLAUDE.md. If not, role
  briefs include the principles explicitly.
- Whether a plugin install keeps symlinks into `core/`. If not, a sync script
  copies `core/` into the adapter.
- Whether TLA+ tools are installed. Until then the formal tier falls back to
  property tests, and the review says so.
