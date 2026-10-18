# frontend-ux: patterns

| Pattern | Earns its place when | Plain form |
|---|---|---|
| State machine for a flow | a flow has more than three states or async steps | a transition map and one step function |
| Optimistic update with rollback | latency would make the UI feel stuck | apply locally, confirm or roll back with a visible message |
| Container and presentational split | data loading and rendering change for different reasons | one component fetches, one renders from props |
| Shared component | the same control appears in two places | a component in the design system, not a copy |
| Portal for overlays | a popover must escape a scrolling or clipped parent | render into a top-level layer |
