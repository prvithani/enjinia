Flow steps 4-5: inbox reaches past notification-store's `exposes`
(unread-for, mark-read!): it filters the whole synced table on the client and
writes read_at directly. Principles: encapsulation; and INV-1 is broken in
practice (every client receives every notification), so Critical.
