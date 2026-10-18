# Spike

Role: `roles/spike.md`, spawned.
Trigger: a decision depends on a number or a behavior that docs and code
cannot answer.

Brief: the one question, why it matters (which ADR or invariant), the time
box, and where to write. The spike writes throwaway code only in a scratch
folder, never in the target repo's tracked files.

Output: `<feature-dir>/spikes/<name>.md`: question, method, raw result
(command and output), answer in one sentence, and how sure (measured or
hypothesis). The finding goes into the ADR that asked for it.
