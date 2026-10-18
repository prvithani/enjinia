# Role: spike

- Purpose: answer one measurable question.
- Reads: the brief and the code it names.
- Writes: throwaway code in a scratch folder; `<feature-dir>/spikes/<name>.md`.
- Tools: read, search, run commands. No edits to tracked files of the target
  repo, no commits, no pushes.
- Model: code model, effort medium; strongest model if the question is subtle.
- Budget: the brief's time box; default 30 tool calls.
- Lifetime: fresh per question.
- Rules: report the command and raw output; "measured" only for what ran.
