# Replay eval rubric

Fixed before any run. A grader applies it to one replayed ticket: Enjinia's
artifacts (`run/`) against what shipped (`oracle/`: the full ticket, the
shipped spec and code, follow-up fixes) and later history in the repo.

## Scores

1. Requirements (0-3). List each requirement the shipped work met (from the
   full ticket and spec). Mark each: captured, missed, or contradicted.
   3 = all captured, none contradicted; 0 = the core one missed.
2. Invariants (0-3). List the invariants the shipped design relies on
   (stated or implied by its tests). Mark each: stated by Enjinia, implied,
   missing. Also list invariants Enjinia stated that the shipped design
   lacks, and whether each is real.
3. Key decisions. List the shipped design's 3-5 key decisions. For each,
   Enjinia's choice: same (2), different and defensible with evidence from
   the code (2), different and worse (0), absent (0). Name the code that
   makes a difference defensible or worse.
4. Defects (-2 to +2). For each follow-up fix in the area after the ship
   (commits, tickets): did Enjinia's design avoid it (+1), share it (0), or
   not touch that area (n/a)? For each defect in Enjinia's design that the
   shipped design does not have: -1.

## Process notes (not scored)

- Interview questions the oracle refused as design questions (count, quote).
- Scope Enjinia added beyond the problem.
- Where Enjinia's stages ran long or circled.

## Verdict

One of: matches, better, worse, mixed. Three sentences, each citing a file.
