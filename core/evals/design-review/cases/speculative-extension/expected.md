Component `delivery-channel` (with `in-app-channel`): a protocol with one
implementation, justified by email/push/Slack, which NG-1 excludes; no ADR
names a second user. Principle: YAGNI (extension point without two users).
Also the Strategy pattern fails its "two behaviors today" test.
