# Design: notifications

## Components

```yaml
components:
  - name: notification-store
    layer: persistence
    kind: mechanism
    responsibility: Stores notifications and read marks; every read and every push to a client (unread-for, subscribe) returns only rows whose recipients include that user.
    owns: [notification, read-mark]
    exposes: [insert!, unread-for, mark-read!, subscribe]
    depends_on: []
    realizes: [FR-1, FR-2, INV-1, INV-2]
    pattern: none
    domain: backend
    enforces: [INV-1, INV-2]
    second_user: run failures and removal approvals use insert! unchanged.
  - name: notify
    layer: domain
    kind: mechanism
    responsibility: Creates a notification for a user or for the users with access to a subject.
    owns: []
    exposes: ["notify! [recipient kind text link]"]
    depends_on: [notification-store, subject-access]
    realizes: [FR-1]
    pattern: none
    domain: backend
    second_user: run failures will call notify! with their own kind and text; notify knows no kinds.
  - name: subject-access
    layer: domain
    kind: policy
    responsibility: Existing access rules; answers which users may read a subject.
    owns: [subject-acl]
    exposes: [users-with-access]
    depends_on: []
    realizes: [FR-1]
    pattern: none
    domain: backend
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
  - name: family-notices
    layer: domain
    kind: policy
    responsibility: Decides when a family redeploy or failure notifies its owners, and the words.
    owns: []
    exposes: [on-family-event]
    depends_on: [notify]
    realizes: [FR-4]
    pattern: none
    domain: backend
  - name: delivery-channel
    layer: domain
    kind: mechanism
    responsibility: A protocol for delivering a notification over a channel, so email, push or Slack can be added later.
    owns: []
    exposes: ["DeliveryChannel protocol: deliver! [channel notification]"]
    depends_on: []
    realizes: [FR-1]
    pattern: "Strategy: channels are chosen per user"
    domain: backend
  - name: in-app-channel
    layer: domain
    kind: policy
    responsibility: The only DeliveryChannel implementation; inserts into the store.
    owns: []
    exposes: [in-app]
    depends_on: [delivery-channel, notification-store]
    realizes: [FR-1]
    pattern: none
    domain: backend
```

## Flows

1. A family event reaches family-notices.on-family-event.
2. family-notices calls notify/notify! with the owners, a kind and the text.
3. notify calls notification-store/insert!.
4. inbox holds notification-store/subscribe for the signed-in user; the
   store pushes only rows whose recipients include that user; inbox shows a
   toast.
5. The user opens the inbox; inbox calls unread-for and mark-read!.
