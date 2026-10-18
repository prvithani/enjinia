The "who may see this notification" rule lives twice: notification-store
(recipients at insert) and inbox (subject ACL at render), and they disagree
once access changes. Principles: DRY (one rule, two places) and INV-1 (the
store's rule is not the one users see). Consequence: a third reader (email
later, an API) must copy the client rule.
