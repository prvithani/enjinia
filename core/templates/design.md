# Design: <feature label>

Status: draft | approved <date>

## Overview

<the shape of the solution in a few sentences; which concept it realizes>

## Components

<!-- trace_check reads this block. Fields:
     name, layer (pack layers.yaml), kind (mechanism | policy | glue),
     responsibility (one sentence), owns (data entities), exposes (contract),
     depends_on (component names), realizes (requirement and invariant ids),
     pattern (name and reason, or none), domain (pack), second_user
     (mechanism only), enforces (invariant ids; say how in responsibility). -->

```yaml
components:
  - name: <name>
    layer: domain
    kind: policy
    responsibility: <one sentence>
    owns: []
    exposes: []
    depends_on: []
    realizes: [FR-1]
    pattern: none
    domain: backend
    enforces: []
```

## Flows

<one numbered sequence per main flow, naming components and contracts>

## Slices

<each slice usable on its own; the first is the walking skeleton>

| Slice | Delivers | Components | Usable because |
|---|---|---|---|

## Existing code

<existing mode: what is refactored first (as its own slice) and why>
