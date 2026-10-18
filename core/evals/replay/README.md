# Replay eval

Does Enjinia design the way the human does? Run stages 0-3 on a shipped
ticket from the code as it was before the work, then compare with what
shipped.

## Method

1. Input: the ticket's problem and done-when only. Ticket texts often carry
   the shipped design ("Build:", "Proposal", "Fix:"); strip it.
2. Codebase: a plain snapshot (`git archive <commit-before-the-work>`), no
   history, so later commits cannot leak.
3. Phase A: the replay lead runs triage, as-is and draft requirements, and
   writes its interview questions.
4. An oracle agent holds the full ticket and the shipped spec and code, and
   answers only at the level of requirements; it refuses design questions.
5. Phase B: the lead finishes requirements, concept (with model checking)
   and design at L3, with no human.
6. A grader applies `rubric.md` (fixed before any run) with the shipped
   work and later fixes in the repo as the answer key.

Artifacts of employer code stay on the employer side (an ignored or
untracked scratch folder there), never in this repo. This folder keeps the
method, the rubric and code-free results.

## Known weaknesses

- An oracle can leak the design through a requirement-level answer that
  names the unit of change (seen once: "a save deploys only the edited
  model"). Graders discount decisions that follow from such a hint.
- One run per ticket, one model: no variance measured.
- The human has not yet checked a grader by grading one ticket by hand.
