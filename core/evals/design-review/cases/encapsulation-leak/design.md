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
```

## Flows

1. A family event reaches family-notices.on-family-event.
2. family-notices calls notify/notify! with the owners, a kind and the text.
3. notify calls notification-store/insert!.
4. The replica syncs the notifications table to every open client.
5. inbox filters the synced notifications table on the client by
   recipients, and writes read_at on the row itself for mark-as-read.
