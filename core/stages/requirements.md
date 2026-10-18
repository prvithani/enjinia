# Stage 1: requirements

Role: `roles/requirements-analyst.md`, run by the lead (it talks to the human).
Output: `<feature-dir>/requirements.md` from `templates/requirements.md`.

1. Draft requirements from the ticket, linked docs and `as-is.md` before
   asking anything. Each one gets an id: `BR-` business, `FR-` functional,
   `NFR-` non-functional, `TR-` technical, `G-` goal, `NG-` non-goal,
   `EB-` existing behavior that must not change. Packs add prefixes.
2. Mark each draft requirement `source:` ticket, doc (path), code (file:line)
   or `assumed`.
3. Interview in rounds of at most 4 questions. Ask only what the documents
   and code cannot answer. Ask about intent and limits: guarantees, bounds
   (freshness, cost, time), what users expect to see, which failure is least
   bad. Test each question: would it still make sense if no design had been
   proposed? If not, it is a design question in disguise. Never offer fix
   options (from a review, a ticket or your own idea) as the answers.
4. Stop interviewing when a round changes no id. At most 3 rounds; then list
   what is still open.
5. Every `assumed` requirement is either confirmed or listed as open.

Gate: the human approves `requirements.md` and the autonomy level. A
requirement never changes after the gate without a new gate.
