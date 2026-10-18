# frontend-ux: concept

- Information architecture: what pages or panels exist, what each shows,
  how users move between them.
- A UI state chart per flow: states, events, transitions, including empty,
  loading, error and offline; optimistic updates and their rollback.
- The interaction model: what each control does, what feedback it gives,
  what is undoable.

Invariants worth stating: the UI never shows a change as saved that the
server did not store; every error state tells the user what happened and
what to do; every action is reachable by keyboard.
