"""Self-check for trace_check: a clean spec has no gap; each mutation of it
produces exactly the gaps that a reviewer would expect, and no others.

Run: python3 core/scripts/tests/test_trace_check.py
"""
import contextlib
import io
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import trace_check  # noqa: E402

CLEAN = HERE / "fixtures" / "clean"
TEST_FILE = "test/ingest/core_test.clj"


def run(edits):
    """Copy the clean fixture, apply {file: (old, new)} edits, return gap kinds."""
    with tempfile.TemporaryDirectory() as tmp:
        spec = Path(tmp) / "spec"
        shutil.copytree(CLEAN, spec)
        for name, (old, new) in edits.items():
            f = spec / name
            text = f.read_text()
            assert old in text, f"fixture edit did not apply: {name}: {old!r}"
            f.write_text(text.replace(old, new, 1))
        _, gaps, _ = trace_check.check(spec, [spec / "test"], [spec / "report.xml"])
        return {g.kind for g in gaps}


# Each case: edits to the clean fixture -> the exact set of gap kinds.
CASES = {
    "duplicate-id": (
        {"requirements.md": ("- FR-1:", "- BR-1: again\n- FR-1:")},
        {"duplicate-id"}),
    "invariant-covers-unknown": (
        {"concept.md": ("covers: [BR-1]", "covers: [BR-1, BR-9]")},
        {"invariant-covers-unknown"}),
    "formal-without-model": (
        {"concept.md": ("    model: models/ingest.tla\n", "")},
        {"formal-without-model"}),
    "component-unknown-dependency": (
        {"design.md": ("depends_on: [inbox]\n    realizes: [FR-1", "depends_on: [inbox, cache]\n    realizes: [FR-1")},
        {"component-unknown-dependency"}),
    "component-cycle": (
        {"design.md": ("owns: [inbox-row]\n    depends_on: []", "owns: [inbox-row]\n    depends_on: [ingress]")},
        {"component-cycle"}),
    "duplicate-component": (
        {"design.md": ("  - name: applier", "  - name: ingress")},
        {"duplicate-component"}),
    "forbidden-layer-dependency": (
        {"design.md": ("owns: [order]\n    depends_on: [inbox]", "owns: [order]\n    depends_on: [inbox, ingress]")},
        {"forbidden-layer-dependency"}),
    "component-realizes-nothing": (
        {"design.md": ("realizes: [INV-1]", "realizes: []")},
        {"component-realizes-nothing", "requirement-without-component"}),
    "component-realizes-unknown": (
        {"design.md": ("realizes: [INV-1]", "realizes: [INV-1, INV-9]")},
        {"component-realizes-unknown"}),
    "entity-has-several-owners": (
        {"design.md": ("owns: [order]", "owns: [order, inbox-row]")},
        {"entity-has-several-owners"}),
    "ambiguous-test-name": (
        {TEST_FILE: ("(deftest ^{:covers [:FR-1]} accepts-valid", "(deftest ^{:covers [:FR-1]} apply-once")},
        {"ambiguous-test-name", "task-test-missing"}),
    "test-covers-unknown": (
        {TEST_FILE: ("[:FR-1]", "[:FR-1 :FR-9]")},
        {"test-covers-unknown"}),
    "invariant-without-test": (
        {TEST_FILE: ("[:INV-1 :BR-2]", "[:BR-2]")},
        {"invariant-without-test"}),
    "task-unknown-dependency": (
        {"tasks.yaml": ("depends_on: [T1]\n  covers: [FR-1]", "depends_on: [T1, T9]\n  covers: [FR-1]")},
        {"task-unknown-dependency"}),
    "task-cycle": (
        {"tasks.yaml": ("- id: T1\n  slice: S1\n  depends_on: []", "- id: T1\n  slice: S1\n  depends_on: [T2]")},
        {"task-cycle"}),
    "duplicate-task": (
        {"tasks.yaml": ("- id: T3", "- id: T2")},
        {"duplicate-task"}),
    "task-covers-nothing": (
        {"tasks.yaml": ("covers: [FR-1]", "covers: []")},
        {"task-covers-nothing", "requirement-without-task"}),
    "task-covers-unknown": (
        {"tasks.yaml": ("covers: [FR-1]", "covers: [FR-1, FR-9]")},
        {"task-covers-unknown"}),
    "task-test-missing": (
        {"tasks.yaml": ("tests: [accepts-valid]", "tests: [accepts-valid, rejects-bad-sig]")},
        {"task-test-missing"}),
    "requirement-without-component": (
        {"design.md": ("realizes: [FR-1, INV-2]", "realizes: [INV-2]")},
        {"requirement-without-component"}),
    "requirement-without-test": (
        {TEST_FILE: ("(deftest ^{:covers [:FR-1]} accepts-valid (is true))\n", ""),
         "tasks.yaml": ("tests: [accepts-valid]", "tests: []")},
        {"requirement-without-test"}),
    "requirement-without-task": (
        {"tasks.yaml": ("covers: [FR-1]", "covers: [INV-2]")},
        {"requirement-without-task"}),
    "requirement-not-passing (failing test)": (
        {"report.xml": ('name="apply-once"/>', 'name="apply-once"><failure/></testcase>')},
        {"requirement-not-passing"}),
    "requirement-not-passing (test not run)": (
        {"report.xml": ('<testcase classname="ingest.core-test" name="accepts-valid"/>', "")},
        {"requirement-not-passing"}),
    "non-goal needs no coverage": (
        {"requirements.md": ("- NG-1:", "- NG-2: Multi-region.\n- NG-1:")},
        set()),
}


def cli(args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return trace_check.main(args)


def main():
    assert run({}) == set(), f"clean fixture has gaps: {run({})}"
    gap_kinds = {k.split(" (")[0] for k, (_, want) in CASES.items() if want}
    for name, (edits, want) in CASES.items():
        got = run(edits)
        assert got == want, f"{name}: want {sorted(want)}, got {sorted(got)}"

    _, _, layers = trace_check.check(CLEAN, [CLEAN / "test"], [CLEAN / "report.xml"])
    assert layers == [["T1"], ["T2", "T3"]], f"task layers: {layers}"

    full = [str(CLEAN), "--tests", str(CLEAN / "test"), "--report", str(CLEAN / "report.xml")]
    assert cli(full) == 0, "clean spec must exit 0"
    no_report = [str(CLEAN), "--tests", str(CLEAN / "test")]
    assert cli(no_report) == 1, "missing evidence is a stage 5 gap"
    assert cli(no_report + ["--stage", "4"]) == 0, "--stage 4 ignores stage 5 gaps"

    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "spec"
        shutil.copytree(CLEAN, bad)
        (bad / "tasks.yaml").write_text("- id: [unclosed\n")
        assert cli([str(bad)]) == 2, "unreadable input must exit 2, not report gaps"

    print(f"ok: clean spec, {len(CASES)} mutations covering {len(gap_kinds)} gap kinds, CLI exit codes")


if __name__ == "__main__":
    main()
