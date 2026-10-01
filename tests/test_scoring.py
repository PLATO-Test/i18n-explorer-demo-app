"""Tests for the scoring package, using synthetic findings fixtures under
tests/scoring_fixtures/ (never the real ground truth text verbatim beyond
what's needed to exercise the matcher - these fixtures are answer-key
adjacent and must never leave this repo, see CLAUDE.md)."""
from pathlib import Path

import pytest

from scoring.findings import FindingsValidationError, load_runs
from scoring.ground_truth import load_controls, load_defects, load_known_issues
from scoring.matcher import score_run
from scoring.report import build_report

FIXTURES = Path(__file__).resolve().parent / "scoring_fixtures"


@pytest.fixture(scope="module")
def defects():
    return load_defects()


@pytest.fixture(scope="module")
def controls():
    return load_controls()


@pytest.fixture(scope="module")
def known_issues():
    return load_known_issues()


def _score(filename: str, build: str, defects, controls, known_issues=()):
    [run] = load_runs(FIXTURES / filename)
    return score_run(run, defects, controls, build, known_issues)


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


def test_a07_matches_regardless_of_category(defects, controls):
    rr = _score("seeded_a07_category_variants.json", "seeded", defects, controls)
    assert rr.detected == {"A07": [0, 1]}
    assert rr.control_fp == {}
    assert rr.unclassified == []


def test_c11_control_fp_regardless_of_category(defects, controls):
    rr = _score("clean_c11_category_variants.json", "clean", defects, controls)
    assert rr.detected == {}
    assert rr.control_fp == {"C11": [0, 1]}
    assert rr.unclassified == []


def test_known_issue_matches_only_for_listed_category(defects, controls, known_issues):
    rr = _score("clean_known_issues.json", "clean", defects, controls, known_issues)
    assert rr.known_issue == {"U01": [0], "U02": [1]}
    assert rr.control_fp == {"C08b": [2]}  # wrong category (plural) falls through to the control
    assert rr.unclassified == []

    runs = load_runs(FIXTURES / "clean_known_issues.json")
    report = build_report(runs, defects, controls, "clean", known_issues)
    source = report["sources"]["ai_judge"]
    assert {ki["issue_id"]: ki["count"] for ki in source["known_issues"]} == {"U01": 1, "U02": 1}
    assert source["false_positive_count"] == 1  # only the C08b hit; known-issue hits don't count


def test_seeded_defect_wins_over_known_issue_at_same_testid(defects, controls, known_issues):
    rr = _score("seeded_known_issue_precedence.json", "seeded", defects, controls, known_issues)
    assert rr.detected == {"A06": [0]}
    assert rr.known_issue == {}


@pytest.mark.parametrize("build", ["seeded", "clean"])
def test_known_issue_path_prefix_matches_unmapped_fr_paths(defects, controls, known_issues, build):
    rr = _score("known_issue_path_prefix.json", build, defects, controls, known_issues)
    assert rr.known_issue == {"U03": [0, 1, 2]}
    assert rr.detected == {}
    assert rr.control_fp == {}
    # wrong category, /en/ path, mapped fr page, and "/frost" (prefix is "/fr/") all fall through
    assert rr.unclassified == [3, 4, 5, 6]


@pytest.mark.parametrize("build", ["seeded", "clean"])
def test_known_issue_u04_matches_both_locales_and_builds(defects, controls, known_issues, build):
    rr = _score("known_issue_calculator_button.json", build, defects, controls, known_issues)
    assert rr.known_issue == {"U04": [0, 1]}
    assert rr.detected == {}
    assert rr.control_fp == {}
    assert rr.unclassified == [2, 3]  # wrong category, wrong page


def test_known_issue_u03_also_claims_unmapped_200_pages(defects, controls, known_issues):
    # Documented over-match (see known_issues.yaml): /fr/application/<other id>
    # renders a real page but is not in the page map.
    rr = _score("known_issue_unmapped_200_page.json", "clean", defects, controls, known_issues)
    assert rr.known_issue == {"U03": [0]}


@pytest.mark.parametrize("build", ["seeded", "clean"])
def test_known_issue_u05_matches_amount_field_only(defects, controls, known_issues, build):
    rr = _score("known_issue_apply_amount.json", build, defects, controls, known_issues)
    assert rr.known_issue == {"U05": [0, 1]}
    assert rr.detected == {}
    assert rr.control_fp == {}
    assert rr.unclassified == [2, 3, 4, 5]  # wrong category, /en/ page, other element, no testid


@pytest.mark.parametrize("build", ["seeded", "clean"])
def test_known_issue_u06_matches_calculator_modal_both_locales(defects, controls, known_issues, build):
    rr = _score("known_issue_calculator_modal.json", build, defects, controls, known_issues)
    assert rr.known_issue == {"U06": [0, 1, 2]}
    assert rr.detected == {}
    assert rr.control_fp == {}
    assert rr.unclassified == [3, 4]  # wrong category, wrong page
