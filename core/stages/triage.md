# Stage 0: triage

Input: a ticket (tracker id or text), a review finding, or a request.
Output: `<feature-dir>/triage.md` from `templates/triage.md`.

1. Read the ticket and everything it links. Summarize the problem in at most
   5 lines, in the human's vocabulary.
2. Mode: `new` or `existing` codebase.
3. Entry point. Usually stage 1. A finding from a review of existing code
   enters at the stage where the defect was born (for example a missing
   invariant enters at stage 2), with stage 1 limited to the requirements
   that defect touches.
4. Size: `small` (one component, no new invariant: skip stages 2-3),
   `medium`, or `large`. State the reason.
5. Packs: the domain packs that apply. `backend` is the default.
6. Blast radius (existing mode): the namespaces, data and contracts the
   change can affect, each with file:line.
7. Ownership: who else works on the same code now (another session, an open
   branch). If someone does, the run is read-only on that code and
   `<feature-dir>` is outside their working tree or in an ignored folder.
8. Horizon: search for proposed or in-flight designs on the same area
   (specs with a Proposed status, related or blocking tickets). Record
   whether this work is the target design or a stopgap until one lands, and
   how long the stopgap may live.
9. Terms: list words the area uses with more than one meaning, and define
   each before stage 1 uses it.
10. Autonomy: propose a level with one sentence of reason.

Gate: none. Triage is reported with stage 1.
