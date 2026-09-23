"""Matches findings from one run against the ground truth for a given
build. See CLAUDE.md / the scorer README section for the matching rules
this implements."""
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from scoring.findings import Finding, Run
from scoring.ground_truth import Entry, KnownIssue, controls_holding_in
from scoring.normalize import normalize_text

# Entries whose fr_seeded text can't be used for the testid-less text
# fallback: D07's is the bare string "en" (would substring-match almost
# any French text), and A06's is an image filename, not rendered text.
# Both are instead matched by category on their own page.
FALLBACK_OVERRIDES: dict[str, Callable[[Finding], bool]] = {
    "A06": lambda f: f.category == "image_text",
    "D07": lambda f: f.category == "lang_attribute",
}


def _match_one(finding: Finding, entries: list[Entry], text_field: str) -> Entry | None:
    if finding.data_testid is not None:
        for entry in entries:
            if finding.page_path in entry.page_paths and finding.data_testid in entry.testids:
                return entry
        return None

    for entry in entries:
        if finding.page_path not in entry.page_paths:
            continue
        override = FALLBACK_OVERRIDES.get(entry.id)
        if override is not None:
            if override(finding):
                return entry
            continue
        needle = normalize_text(getattr(entry, text_field))
        if needle and needle in normalize_text(finding.observed):
            return entry
    return None


def _match_known_issue(finding: Finding, issues: list[KnownIssue]) -> KnownIssue | None:
    if finding.data_testid is None:
        return None
    for issue in issues:
        if (
            finding.page_path in issue.page_paths
            and finding.data_testid in issue.testids
            and finding.category in issue.categories
        ):
            return issue
    return None


@dataclass
class RunResult:
    run: Run
    build: str
    detected: dict[str, list[int]]  # defect id -> matching finding indices
    known_issue: dict[str, list[int]]  # known-issue id -> matching finding indices
    control_fp: dict[str, list[int]]  # control id -> matching finding indices
    unclassified: list[int]  # finding indices


def score_run(
    run: Run,
    defects: list[Entry],
    controls: list[Entry],
    build: str,
    known_issues: list[KnownIssue] = (),
) -> RunResult:
    active_defects = defects if build == "seeded" else []
    active_controls = controls_holding_in(controls, build)
    text_field = "fr_clean" if build == "clean" else "fr_seeded"

    detected: dict[str, list[int]] = defaultdict(list)
    known_issue_hits: dict[str, list[int]] = defaultdict(list)
    control_fp: dict[str, list[int]] = defaultdict(list)
    unclassified: list[int] = []

    for i, finding in enumerate(run.findings):
        entry = _match_one(finding, active_defects, text_field)
        if entry is not None:
            detected[entry.id].append(i)
            continue
        issue = _match_known_issue(finding, known_issues)
        if issue is not None:
            known_issue_hits[issue.id].append(i)
            continue
        entry = _match_one(finding, active_controls, text_field)
        if entry is not None:
            control_fp[entry.id].append(i)
            continue
        unclassified.append(i)

    return RunResult(
        run=run,
        build=build,
        detected=dict(detected),
        known_issue=dict(known_issue_hits),
        control_fp=dict(control_fp),
        unclassified=unclassified,
    )
