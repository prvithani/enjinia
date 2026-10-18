# database: concept

The logical model first: entities, keys, relationships, and the
invariants the data must keep. Then the physical model: tables, the
constraints that enforce each invariant, and the indexes the access
patterns need.

Rule: an invariant the database can enforce (unique, foreign key, check,
not null) is enforced there, not only in application code; the concept
says which constraint enforces which invariant. When the database cannot
enforce it (ordering at boot, cross-row rules), the concept says what does,
and the formal tier may apply (one trial found a unique constraint could
keep a name unique but could not make its holder the right kind of row).
