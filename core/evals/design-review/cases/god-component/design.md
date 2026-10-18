# Design: notifications

## Components

```yaml
components:
  - name: notification-store
    layer: persistence
    kind: mechanism
    responsibility: Stores notifications and read marks; returns only rows whose recipients include the asking user.
    owns: [notification, read-mark]
    exposes: [insert!, unread-for, mark-read!]
    depends_on: []
    realizes: [FR-2, INV-1, INV-2]
    pattern: none
    domain: backend
    enforces: [INV-1, INV-2]
  - name: notifications
    layer: domain
    kind: mechanism
    responsibility: Creates notifications, decides which family events notify owners and with what words, chooses whether the client shows a toast, and retries delivery to open clients.
    owns: []
    exposes: ["notify! [recipient kind text link]", on-family-event, "toast?"]
    depends_on: [notification-store]
    realizes: [FR-1, FR-3, FR-4, NFR-1]
    pattern: none
    domain: backend
  - name: inbox
    layer: ui
    kind: glue
    responsibility: Shows unread notifications and marks them read.
    owns: []
    exposes: [inbox-view]
    depends_on: [notification-store, notifications]
    realizes: [FR-2]
    pattern: none
    domain: frontend-ux
```

## Flows

1. A family event reaches notifications.on-family-event, which picks owners and words and calls notify!.
2. notify! calls notification-store/insert!.
3. The client asks notifications/toast? and shows a toast.
4. The user opens the inbox; inbox calls unread-for and mark-read!.
