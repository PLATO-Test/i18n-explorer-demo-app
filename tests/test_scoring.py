"""Tests for the scoring package, using synthetic findings fixtures under
tests/scoring_fixtures/ (never the real ground truth text verbatim beyond
what's needed to exercise the matcher - these fixtures are answer-key
adjacent and must never leave this repo, see CLAUDE.md)."""
from __future__ import annotations

from pathlib import Path

import pytest

from scoring.findings import FindingsValidationError, load_runs
from scoring.ground_truth import load_controls, load_defects
from scoring.matcher import score_run
from scoring.report import build_report

FIXTURES = Path(__file__).resolve().parent / "scoring_fixtures"


@pytest.fixture(scope="module")
def defects():
    return load_defects()


@pytest.fixture(scope="module")
def controls():
    return load_controls()


def _score(filename: str, build: str, defects, controls):
    [run] = load_runs(FIXTURES / filename)
    return score_run(run, defects, controls, build)


def test_all_defects_detected_gives_recall_one(defects, controls):
    runs = load_runs(FIXTURES / "seeded_all_detected.json")
    report = build_report(runs, defects, controls, "seeded")
    source = report["sources"]["deterministic"]
    assert source["recall"] == 1.0
    assert all(row["detected"] for row in source["defect_table"])
    assert all(row["category_correct"] for row in source["defect_table"])


def test_no_findings_gives_recall_zero(defects, controls):
    runs = load_runs(FIXTURES / "seeded_no_findings.json")
    report = build_report(runs, defects, controls, "seeded")
    source = report["sources"]["deterministic"]
    assert source["recall"] == 0.0
    assert all(not row["detected"] for row in source["defect_table"])


def test_finding_on_control_is_a_false_positive(defects, controls):
    rr = _score("seeded_control_fp.json", "seeded", defects, controls)
    assert rr.detected == {}
    assert rr.unclassified == []
    assert "C01" in rr.control_fp
    assert rr.control_fp["C01"] == [0]


def test_null_testid_finding_matched_via_text_fallback(defects, controls):
    rr = _score("seeded_text_fallback.json", "seeded", defects, controls)
    assert rr.detected == {"D01": [0]}


def test_fallback_overrides_for_a06_and_d07(defects, controls):
    rr = _score("seeded_fallback_overrides.json", "seeded", defects, controls)
    assert rr.detected == {"A06": [0], "D07": [1]}


def test_duplicate_finding_counted_once(defects, controls):
    rr = _score("seeded_duplicate.json", "seeded", defects, controls)
    assert list(rr.detected.keys()) == ["D01"]
    assert rr.detected["D01"] == [0, 1]  # both findings kept, but one detection

    runs = load_runs(FIXTURES / "seeded_duplicate.json")
    report = build_report(runs, defects, controls, "seeded")
    source = report["sources"]["ai_explorer"]
    d01_row = next(r for r in source["defect_table"] if r["id"] == "D01")
    assert d01_row["detected"] is True
    assert len(d01_row["matched_findings"]) == 2  # both findings on record...
    assert source["recall"] == 1 / len(defects)  # ...but only 1 of N defects detected


def test_invalid_file_rejected_with_clear_error():
    with pytest.raises(FindingsValidationError) as exc_info:
        load_runs(FIXTURES / "invalid_missing_field.json")
    message = str(exc_info.value)
    assert "invalid_missing_field.json" in message
    assert "expected" in message or "evidence" in message


def test_clean_build_every_finding_is_fp_or_unclassified(defects, controls):
    rr = _score("clean_fp_and_unclassified.json", "clean", defects, controls)
    assert rr.detected == {}  # defects.yaml is never matched against in clean mode
    assert "C05" in rr.control_fp  # hit a control testid -> false positive
    assert len(rr.unclassified) == 2  # made-up field + hallucinated D01 hit

    runs = load_runs(FIXTURES / "clean_fp_and_unclassified.json")
    report = build_report(runs, defects, controls, "clean")
    source = report["sources"]["deterministic"]
    assert source["defect_table"] is None
    assert source["recall"] is None
    assert source["precision"] is None
    assert source["false_positive_count"] == 3  # 1 control FP + 2 unclassified


def test_stability_computed_across_three_runs(defects, controls):
    runs = load_runs(FIXTURES / "stability")
    assert len(runs) == 3
    report = build_report(runs, defects, controls, "seeded")
    source = report["sources"]["ai_judge"]
    stability = source["stability"]
    assert stability["D01"] == {"detected_runs": 3, "total_runs": 3}
    assert stability["D02"] == {"detected_runs": 2, "total_runs": 3}
    assert stability["D03"] == {"detected_runs": 1, "total_runs": 3}
    assert stability["D04"] == {"detected_runs": 0, "total_runs": 3}
