# Design reviewer calibration

One feature (server-originated notifications), one good design and five
designs with one planted defect each, for the judgment rows of
`core/principles.md`. Structural defects (cycles, two owners) are
`trace_check.py`'s and are not here.

Pass: the reviewer reports the planted defect (right component and
principle) as Critical or Important in each bad design, and no Critical or
Important finding on `good`. Nits are allowed and counted.

Run: one fresh `design-reviewer` per case, with `requirements.md`,
`concept.md`, `cases/<case>/design.md` and `core/principles.md`. The
expected finding for each case is in `cases/<case>/expected.md`; never give
it to the reviewer.
