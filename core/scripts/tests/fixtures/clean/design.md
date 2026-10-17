# Design

```yaml
components:
  - name: ingress
    layer: infra
    owns: [webhook-request]
    depends_on: [inbox]
    realizes: [FR-1, INV-2]
  - name: inbox
    layer: persistence
    owns: [inbox-row]
    depends_on: []
    realizes: [INV-2]
  - name: applier
    layer: domain
    owns: [order]
    depends_on: [inbox]
    realizes: [INV-1]
```
