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
    realizes: [FR-1, FR-2, INV-1, INV-2]
    pattern: none
    domain: backend
    enforces: [INV-1, INV-2]
  - name: notify
    layer: domain
    kind: mechanism
    responsibility: Creates a notification; the kind is one of :family-redeployed or :family-failed, and notify builds the text from the family's name and last error.
    owns: []
    exposes: ["notify! [family-id kind]"]
    depends_on: [notification-store]
    realizes: [FR-1, FR-4]
    pattern: none
    domain: backend
    second_user: run failures will add their kinds to notify's kind list.
  - name: inbox
    layer: ui
    kind: glue
    responsibility: Shows unread notifications, marks them read, and toasts new ones while the app is open.
    owns: []
    exposes: [inbox-view]
    depends_on: [notification-store]
    realizes: [FR-2, FR-3, NFR-1]
    pattern: none
    domain: frontend-ux
```

## Flows

1. A family event calls notify/notify! with the family id and a kind.
2. notify looks up the owners and builds the text, then calls insert!.
3. The replica syncs the row; inbox shows a toast.
