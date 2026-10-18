Component `notifications`: its responsibility joins four kinds of work
(creation mechanism, family policy, UI decision, delivery retry). Principles:
separation of concerns / single responsibility, and mechanism vs policy (a
mechanism holding family policy). Consequence: a second policy user (run
failures) must edit this component.
