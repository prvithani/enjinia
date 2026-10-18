# backend: spike

A spike answers one measurable question: a latency, a row count, what a
library or database actually does under a given input. Throwaway code in a
scratch folder, never in tracked files; the command and raw output go into
`spikes/<name>.md`, labelled measured or hypothesis.

Typical backend spikes: query plan on realistic volume; behavior of a
database statement under conflict; what a dependency's function returns
for an edge input.
