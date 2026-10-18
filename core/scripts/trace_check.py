#!/usr/bin/env python3
"""Derive the traceability matrix of one feature spec and fail on gaps.

Usage:
  trace_check.py SPEC_DIR [--tests DIR]... [--report JUNIT_XML]...
                 [--stage N] [--layers FILE]

Formats read from SPEC_DIR (see tests/fixtures/clean for an example):
  requirements.md  list items `- BR-1: text`. Any `PREFIX-n` id. `NG-` ids
                   (non-goals) need no coverage.
  concept.md       a ```yaml block with `invariants:`, each
                   {id, covers: [req ids], tier: formal|property|example,
                   model: path (formal tier only, relative to SPEC_DIR)}.
  design.md        a ```yaml block with `components:`, each
                   {name, layer, owns: [entities], depends_on: [names],
                   realizes: [req or invariant ids], kind, enforces:
                   [invariant ids], ...}. Once components exist, every
                   invariant needs a component that enforces it.
  tasks.yaml       list of {id, slice, depends_on, covers, tests, ...}.
Tests: Clojure `(deftest ^{:covers [:BR-1 :INV-2]} name ...)` under --tests.
Report: JUnit XML; a test passes if its testcase has no failure or error.

--stage N fails only on gaps owned by stages 1..N (default 5).
--layers names a YAML file `layers: [names]` and
`forbidden: [[from_layer, to_layer], ...]`.
Records are type-checked (SCHEMAS); a wrong type, missing field or unknown
value exits 2 with every problem listed, so YAML's implicit typing (`no`
read as false, `1.10` as 1.1) fails loudly.
Exit 0 when no gap, 1 on gaps, 2 on unreadable input.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

DEFAULT_LAYERS = Path(__file__).resolve().parents[1] / "packs/backend/layers.yaml"
REQ_ITEM = re.compile(r"^\s*[-*]\s+([A-Z][A-Z0-9]*-\d+)\s*:")
YAML_FENCE = re.compile(r"^```ya?ml\s*\n(.*?)^```", re.M | re.S)
DEFTEST = re.compile(r"\(deftest\s+\^\{[^}]*:covers\s+\[([^\]]*)\][^}]*\}\s+([^\s()]+)")


ID = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
# Per record kind: field -> (type, required). "ids" is a list of requirement or
# invariant ids; "names" a list of strings; a set is an allowed-values enum.
SCHEMAS = {
    "invariant": {"id": ("id", True), "covers": ("ids", True),
                  "tier": ({"formal", "property", "example"}, True), "model": ("str", False)},
    "component": {"name": ("str", True), "layer": ("layer", True), "owns": ("names", False),
                  "depends_on": ("names", False), "realizes": ("ids", False),
                  "kind": ({"mechanism", "policy", "glue"}, False), "enforces": ("ids", False)},
    "task": {"id": ("str", True), "slice": ("str", False), "depends_on": ("names", False),
             "covers": ("ids", False), "tests": ("names", False)},
}


class InputError(Exception):
    """Malformed spec input: wrong types, missing fields, unknown values."""


def validate(kind, records, where, layers):
    """Raise InputError listing every field that breaks SCHEMAS[kind]."""
    if not isinstance(records, list):
        raise InputError(f"{where}: expected a list of {kind}s, got {type(records).__name__}")
    errors = []
    for n, rec in enumerate(records):
        at = f"{where}: {kind} #{n + 1}"
        if not isinstance(rec, dict):
            errors.append(f"{at}: expected a mapping, got {rec!r}")
            continue
        for field, (typ, required) in SCHEMAS[kind].items():
            if field not in rec or rec[field] is None:
                if required:
                    errors.append(f"{at}: missing `{field}`")
                continue
            v = rec[field]
            ok = (isinstance(v, str) and bool(ID.match(v)) if typ == "id" else
                  isinstance(v, str) if typ == "str" else
                  v in layers if typ == "layer" else
                  isinstance(v, list) and all(isinstance(x, str) and (typ == "names" or ID.match(x)) for x in v)
                  if typ in ("ids", "names") else
                  v in typ)
            if not ok:
                want = (f"one of {sorted(layers)}" if typ == "layer" else
                        f"one of {sorted(typ)}" if isinstance(typ, set) else
                        {"id": "an id like BR-1", "str": "a string",
                         "ids": "a list of ids like [BR-1]", "names": "a list of strings"}[typ])
                errors.append(f"{at}: `{field}` is {v!r}; expected {want}")
    if errors:
        raise InputError("\n".join(errors))
    return records


class Gap:
    def __init__(self, stage, kind, detail):
        self.stage, self.kind, self.detail = stage, kind, detail

    def __repr__(self):
        return f"stage {self.stage} {self.kind}: {self.detail}"


def yaml_key(path, key):
    """The value of `key` from the first ```yaml block in `path` that has it."""
    if not path.exists():
        return []
    for block in YAML_FENCE.findall(path.read_text()):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and key in data:
            return data[key] or []
    return []


def read_requirements(path):
    if not path.exists():
        return []
    return [m.group(1) for line in path.read_text().splitlines()
            if (m := REQ_ITEM.match(line))]


def read_tests(dirs):
    """{test name: [covered ids]} from Clojure deftest metadata."""
    tests = {}
    for d in dirs:
        for f in sorted(Path(d).rglob("*.clj*")):
            for covers, name in DEFTEST.findall(f.read_text()):
                ids = [t.lstrip(":") for t in covers.split()]
                tests.setdefault(name, []).append(ids)
    return tests


def read_report(files):
    """{test name: passed} from JUnit XML."""
    result = {}
    for f in files:
        for case in ET.parse(f).getroot().iter("testcase"):
            failed = case.find("failure") is not None or case.find("error") is not None
            name = case.get("name")
            result[name] = result.get(name, True) and not failed
    return result


def topo_layers(deps):
    """Layers of a {node: [deps]} graph; raises ValueError naming a cycle's nodes."""
    remaining = {n: set(ds) for n, ds in deps.items()}
    layers = []
    while remaining:
        ready = sorted(n for n, ds in remaining.items() if not ds & remaining.keys())
        if not ready:
            raise ValueError(sorted(remaining))
        layers.append(ready)
        for n in ready:
            del remaining[n]
    return layers


def duplicates(ids):
    seen, dup = set(), set()
    for i in ids:
        (dup if i in seen else seen).add(i)
    return sorted(dup)


def check_graph(stage, what, deps):
    """Unknown references and cycles in a {node: [deps]} graph."""
    gaps = [Gap(stage, f"{what}-unknown-dependency", f"{n} -> {d}")
            for n, ds in deps.items() for d in ds if d not in deps]
    known = {n: [d for d in ds if d in deps] for n, ds in deps.items()}
    layers = []
    try:
        layers = topo_layers(known)
    except ValueError as e:
        gaps.append(Gap(stage, f"{what}-cycle", ", ".join(e.args[0])))
    return gaps, layers


def check(spec, test_dirs=(), reports=(), layers_file=DEFAULT_LAYERS):
    """Return (rows, gaps, task_layers). Rows are matrix rows, one per requirement."""
    spec = Path(spec)
    reqs = read_requirements(spec / "requirements.md")
    invs = yaml_key(spec / "concept.md", "invariants")
    comps = yaml_key(spec / "design.md", "components")
    tasks_path = spec / "tasks.yaml"
    tasks = (yaml.safe_load(tasks_path.read_text()) or []) if tasks_path.exists() else []
    tests = read_tests(test_dirs)
    report = read_report(reports)
    rules = yaml.safe_load(Path(layers_file).read_text()) or {}
    layer_names = set(rules.get("layers", []))
    forbidden = {tuple(e) for e in rules.get("forbidden", [])}
    validate("invariant", invs, "concept.md", layer_names)
    validate("component", comps, "design.md", layer_names)
    validate("task", tasks, "tasks.yaml", layer_names)

    gaps = []
    inv_ids = [i["id"] for i in invs]
    known_ids = set(reqs) | set(inv_ids)
    gaps += [Gap(1, "duplicate-id", i) for i in duplicates(reqs + inv_ids)]

    # Stage 2: invariants.
    covers_of = {i["id"]: i.get("covers") or [] for i in invs}
    for i in invs:
        gaps += [Gap(2, "invariant-covers-unknown", f"{i['id']} -> {r}")
                 for r in covers_of[i["id"]] if r not in reqs]
        if i.get("tier") == "formal" and not (i.get("model") and (spec / i["model"]).exists()):
            gaps.append(Gap(2, "formal-without-model", i["id"]))

    def expand(ids):
        """Requirement ids reached by `ids` directly or through invariants."""
        out = set()
        for x in ids:
            out.add(x)
            out.update(covers_of.get(x, []))
        return out

    # Stage 3: components and tests.
    comp_deps = {c["name"]: c.get("depends_on") or [] for c in comps}
    graph_gaps, _ = check_graph(3, "component", comp_deps)
    gaps += graph_gaps
    gaps += [Gap(3, "duplicate-component", n) for n in duplicates([c["name"] for c in comps])]
    layer_of = {c["name"]: c.get("layer") for c in comps}
    for c in comps:
        for d in c.get("depends_on") or []:
            if (layer_of[c["name"]], layer_of.get(d)) in forbidden:
                gaps.append(Gap(3, "forbidden-layer-dependency",
                                f"{c['name']} ({layer_of[c['name']]}) -> {d} ({layer_of.get(d)})"))
        realizes = c.get("realizes") or []
        if not realizes:
            gaps.append(Gap(3, "component-realizes-nothing", c["name"]))
        gaps += [Gap(3, "component-realizes-unknown", f"{c['name']} -> {r}")
                 for r in realizes if r not in known_ids]
    owners = {}
    for c in comps:
        for e in c.get("owns") or []:
            owners.setdefault(e, []).append(c["name"])
    gaps += [Gap(3, "entity-has-several-owners", f"{e}: {', '.join(cs)}")
             for e, cs in sorted(owners.items()) if len(cs) > 1]
    gaps += [Gap(3, "ambiguous-test-name", n) for n, v in tests.items() if len(v) > 1]
    test_covers = {n: sorted({i for ids in v for i in ids}) for n, v in tests.items()}
    for n, ids in test_covers.items():
        gaps += [Gap(3, "test-covers-unknown", f"{n} -> {i}") for i in ids if i not in known_ids]
    for i in inv_ids:
        if not any(i in ids for ids in test_covers.values()):
            gaps.append(Gap(3, "invariant-without-test", i))
    enforced = {i for c in comps for i in c.get("enforces") or []}
    if comps:
        gaps += [Gap(3, "invariant-not-enforced", i) for i in inv_ids if i not in enforced]
    for c in comps:
        gaps += [Gap(3, "component-enforces-unknown", f"{c['name']} -> {i}")
                 for i in c.get("enforces") or [] if i not in inv_ids]

    # Stage 4: tasks.
    task_deps = {t["id"]: t.get("depends_on") or [] for t in tasks}
    task_gaps, task_layers = check_graph(4, "task", task_deps)
    gaps += task_gaps
    gaps += [Gap(4, "duplicate-task", n) for n in duplicates([t["id"] for t in tasks])]
    for t in tasks:
        covers = t.get("covers") or []
        if not covers:
            gaps.append(Gap(4, "task-covers-nothing", t["id"]))
        gaps += [Gap(4, "task-covers-unknown", f"{t['id']} -> {c}") for c in covers if c not in known_ids]
        gaps += [Gap(4, "task-test-missing", f"{t['id']} -> {n}")
                 for n in t.get("tests") or [] if n not in tests]

    # Matrix rows; per-requirement gaps for stages 3-5.
    rows = []
    for r in reqs:
        row_invs = [i for i in inv_ids if r in covers_of[i]]
        row_comps = [c["name"] for c in comps if r in expand(c.get("realizes") or [])]
        row_tests = sorted(n for n, ids in test_covers.items() if r in expand(ids))
        row_tasks = [t["id"] for t in tasks if r in expand(t.get("covers") or [])]
        missing = [n for n in row_tests if n not in report]
        failing = [n for n in row_tests if report.get(n) is False]
        evidence = ("fail: " + ", ".join(failing) if failing else
                    "missing: " + ", ".join(missing) if missing else
                    "pass" if row_tests else "")
        rows.append([r, row_invs, row_comps, row_tests, row_tasks, evidence])
        if r.startswith("NG-"):
            continue
        if not row_comps:
            gaps.append(Gap(3, "requirement-without-component", r))
        if not row_tests:
            gaps.append(Gap(3, "requirement-without-test", r))
        if not row_tasks:
            gaps.append(Gap(4, "requirement-without-task", r))
        if row_tests and evidence != "pass":
            gaps.append(Gap(5, "requirement-not-passing", f"{r}: {evidence}"))
    return rows, gaps, task_layers


def render(rows):
    head = ["Requirement", "Invariants", "Components", "Tests", "Tasks", "Evidence"]
    cell = lambda v: (", ".join(v) if isinstance(v, list) else v) or "-"
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("spec")
    p.add_argument("--tests", action="append", default=[])
    p.add_argument("--report", action="append", default=[])
    p.add_argument("--stage", type=int, default=5, choices=range(1, 6))
    p.add_argument("--layers", default=DEFAULT_LAYERS)
    a = p.parse_args(argv)
    try:
        rows, gaps, layers = check(a.spec, a.tests, a.report, a.layers)
    except InputError as e:
        print(f"trace-check: invalid input:\n{e}", file=sys.stderr)
        return 2
    except (OSError, yaml.YAMLError, ET.ParseError) as e:
        print(f"trace-check: cannot read input: {e!r}", file=sys.stderr)
        return 2
    print(render(rows))
    if layers:
        print("\nTask layers:")
        for n, layer in enumerate(layers):
            print(f"  {n}: {', '.join(layer)}")
    active = [g for g in gaps if g.stage <= a.stage]
    print(f"\n{len(active)} gap(s) through stage {a.stage}.")
    for g in sorted(active, key=lambda g: (g.stage, g.kind, g.detail)):
        print(f"  {g!r}")
    return 1 if active else 0


if __name__ == "__main__":
    sys.exit(main())
