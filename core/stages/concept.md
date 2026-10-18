# Stage 2: conceptual design

Role: `roles/concept-modeler.md`, run by the lead.
Output: `<feature-dir>/concept.md` from `templates/concept.md`, models under
`<feature-dir>/models/`, and ADRs under `<feature-dir>/adr/`.

1. Model the problem as concepts: actors, state, operations, and what each
   operation may observe. No technology names unless a requirement fixes one.
2. Write each invariant `INV-n`: one sentence, the requirements it covers,
   and a verification tier:
   - `formal`: state machines, concurrency, crash and retry, money, data
     integrity. Needs a model in `models/` and a model-checker run.
   - `property`: pure logic. Needs a property test (written in stage 3).
   - `example`: everything else.
3. Formal tier. Write the smallest TLA+ model that can break the invariant:
   only the state and steps the invariant depends on, small constants (2
   actors, 2-3 items). Run it with `core/scripts/tlc <model.tla>`.
   - A violation is the most useful result. Keep the trace in
     `models/<name>.trace.txt` and explain it in words.
   - Model each candidate design as its own spec or as a constant switch, and
     check each against the same invariants. A design that passes is
     recorded with the state count; "passes" is only as wide as the model.
   - Read every trace against the code before reporting it. A violation the
     code cannot produce is a model error: fix the model, rerun everything.
   - For every design that passes, run one mutant that must fail (drop one
     check). If the mutant also passes, the model cannot see that check:
     widen it (more items, partitions or actors) before trusting the pass.
   - List every simplification that fixes something the real system varies
     (a constant, a fixed shape, a single instance) and say why a defect
     cannot hide there. If you cannot say why, make it vary in the model.
   - If TLC is not installed, mark the invariant `degraded` and fall back to a
     property test. Say so in the stage report.
4. Estimates (latency, size, cost) are labelled `estimate` with their inputs.
5. A fact the model needs but cannot get from docs or code is a spike:
   `stages/spike.md`.
6. Existing mode: the concept is the difference from `as-is.md`. If a new
   requirement breaks an existing invariant, redesign that part.
7. When candidates compete, write an ADR from `templates/adr.md` with 2-3
   options, the model-checker result of each, and a recommendation.

Gate: the human approves the invariants, tiers and the recommended ADR
option. At L2 the human still approves this gate.
