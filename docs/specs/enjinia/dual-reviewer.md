# Dual reviewer: Claude plus a second vendor

Status: design guide for B. Not built. Claude-only until the calibration below
shows the second reviewer earns its cost.

## Why two reviewers

A reviewer misses defects in patterns. A second reviewer of the same model,
with the same brief, misses the same ones. A model from another vendor has
different blind spots. The gain is the defects only it catches.

Two reviewers also add noise and cost. The protocol below keeps the catches
and filters the noise with evidence, not votes.

## Where it plugs in

Both reviewers are the same role, `reviewer`, run through the same seam:

```
run_role(role="reviewer", brief, files, model="claude-opus-5-5")
run_role(role="reviewer", brief, files, model="<second vendor model>")
```

- The role definition (purpose, inputs, output schema, rules) is shared.
- Each vendor has its own runner in `adapters/<vendor>/`. A runner may call
  the vendor's agent CLI in non-interactive mode or its API SDK. Check the
  vendor's current docs when you build it; this guide does not depend on it.
- A vendor-specific prompt variant is allowed only if the eval shows the
  shared prompt underperforms on that model.

## Protocol

1. **Blind, parallel review.** Both get the same brief: spec sections,
   invariants, the diff or `design.md`, the pragmatic-review rules. Neither
   sees the other's findings.
2. **One finding schema.** Both return JSON:

   ```json
   {"id": "r1-03", "file": "src/applier.clj", "line": 41,
    "severity": "critical", "claim": "effect and status commit separately",
    "evidence": {"kind": "repro", "detail": "prop_apply_once seed 8813"}}
   ```

   `evidence.kind` is `repro`, `measurement` or `rule` (a cited line of
   CLAUDE.md, the spec or an ADR). No evidence, no finding.
3. **Match.** Code matches findings by file and nearby lines. A cheap model
   call decides whether two claims at the same place mean the same defect.
   Matched findings are `agreed`.
4. **Cross-check the rest.** Each unmatched finding goes to the other
   reviewer, read-only: confirm or refute, with evidence. If the finding has a
   runnable repro, the orchestrator runs it, and the result decides. Facts
   that can be executed are never voted on.
5. **Decide.**

   | Situation | Result |
   |---|---|
   | Agreed | accept |
   | One reviewer, confirmed by the other or by a repro | accept |
   | Refuted with evidence | drop, keep in the log |
   | Still unresolved | ❓ to you, both positions side by side |

6. **Severity.** If the two disagree, take the severity whose evidence holds.
   If both hold, take the lower one and flag it.
7. **Fix and re-check.** After fixes, each reviewer re-checks only its own
   accepted findings and any new defect the fix added. Use the same session
   if the runner supports resume; otherwise a fresh run with the finding list.

## When to run the second reviewer

Cost matters, so not everywhere:
- Design review (stage 3), before code exists. Design defects are the most
  expensive.
- Slice review and final review.
- Peer review of formal-tier components (state machines, concurrency, money).
- Not on every peer-review round of ordinary tasks.

## Measure it, then decide

Log per reviewer, per run: findings, confirmed (precision), refuted (noise),
unique confirmed catches, cost and time.

Calibration before turning it on:
- Seeded defect set: bad designs and buggy diffs with known defects, plus
  clean ones (expected result: zero findings).
- Run Claude alone, the second vendor alone, and both with this protocol.
- Keep the second vendor only if it adds unique confirmed catches at a cost
  you accept. Re-check with each model upgrade.

## Failure handling

If the second vendor fails or times out, the run continues with Claude only.
The review is marked `single-reviewer` in `review.md`. Never silently.
