"""Tests for scoring.compare, on a synthetic run laid out like the real one
(<run>/seeded, <run>/clean, judge-manifest.json, explorer/<n>/manifest.json).
Like the scoring fixtures, this is answer-key adjacent (it builds findings
from ground_truth/defects.yaml) and must never leave this repo."""
import json
import shutil
from pathlib import Path

import pytest

from scoring.compare import main
from scoring.ground_truth import load_defects

RUN_BLOCK = {
    "run_id": "synthetic",
    "base_url": "http://localhost:5002",
    "started_at": "2026-09-16T10:00:00Z",
    "model": None,
    "input_tokens": None,
    "output_tokens": None,
    "cost_usd": None,
    "duration_s": 5.0,
}


def _finding(entry) -> dict:
    return {
        "page_path": entry.page_paths[0],
        "data_testid": entry.testids[0] if entry.testids else None,
        "category": entry.category,
        "observed": "x",
        "expected": None,
        "description": "synthetic",
        "severity": "low",
        "evidence": None,
    }


def _write_findings(path: Path, source: str, findings: list[dict], **run) -> None:
    block = {**RUN_BLOCK, "source": source, **run}
    if source != "deterministic":
        block.update(model="claude-sonnet-5", input_tokens=904, output_tokens=100, cost_usd=0.05, duration_s=60.0)
    path.write_text(json.dumps({"run": block, "findings": findings}), encoding="utf-8")


def _explorer_manifest(index: int, status: str) -> dict:
    return {
        "status": status,
        "model_pinned": "claude-sonnet-5",
        "cost_usd": 0.05,
        "cost_basis": "list price, notional on a subscription",
        "duration_s": 60.0,
        "budget_used": {"turns": 10 + index, "tool_calls": 50 + index, "screenshots": index},
        "tokens": {
            "input_tokens": 4,
            "cache_creation_input_tokens": 200,
            "cache_read_input_tokens": 700,
            "output_tokens": 100,
        },
        "model_usage": {
            "claude-sonnet-5": {
                "inputTokens": 4, "cacheCreationInputTokens": 200, "cacheReadInputTokens": 700, "outputTokens": 100,
            },
        },
    }


def _explorer_coverage() -> dict:
    side = {"pages": 5, "pages_reached": 4, "states_configured": 10, "states_reached": 6}
    return {
        "summary": {"en": side, "fr": {**side, "pages_reached": 5, "states_reached": 8}},
        "never_visited": [],
        "visited_paths_not_in_config": [],
    }


@pytest.fixture(scope="module")
def run_dir(tmp_path_factory) -> dict[str, Path]:
    """A synthetic run: deterministic finds the deterministic-layer and 'both'
    defects, the judge the 'ai' and 'both' ones, the explorer the 'ai' ones
    plus D01. Explorer run 3 is rate-limited."""
    root = tmp_path_factory.mktemp("run")
    defects = load_defects()
    found = {
        "deterministic": [d for d in defects if d.expected_layer in ("deterministic", "both")],
        "ai_judge": [d for d in defects if d.expected_layer in ("ai", "both")],
        "ai_explorer": [d for d in defects if d.expected_layer == "ai" or d.id == "D01"],
    }
    calls = {"calls": [{
        "cached": False, "input_tokens": 100, "output_tokens": 10, "cost_usd": 0.01, "duration_s": 1.0,
        "usage_breakdown": {"modelUsage": {"claude-sonnet-5": {"costBasis": "list"}}},
    }]}
    for build in ("seeded", "clean"):
        d = root / build
        d.mkdir()
        (d / "run.json").write_text(json.dumps({"duration_s": 3.0}), encoding="utf-8")
        (d / "calls.json").write_text(json.dumps(calls), encoding="utf-8")
        seeded = build == "seeded"
        _write_findings(d / "findings.json", "deterministic", [_finding(e) for e in found["deterministic"]] if seeded else [])
        judge_files = ["findings-ai-judge-1.json"] + (["findings-ai-judge-2.json", "findings-ai-judge-3.json"] if seeded else [])
        entries = []
        for i, name in enumerate(judge_files, start=1):
            _write_findings(d / name, "ai_judge", [_finding(e) for e in found["ai_judge"]] if seeded else [])
            entries.append({
                "pass": 1, "status": "ok", "file": name, "kind": "single" if i == 1 else "repeat",
                "cache": "used" if i == 1 else "bypassed", "calls": 2, "model_calls": 2, "cache_hits": 0,
                "calls_file": "calls.json",
            })
        (d / "judge-manifest.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
        indexes = (1, 2, 3) if seeded else (1,)
        for i in indexes:
            _write_findings(
                d / f"findings-ai-explorer-{i}.json", "ai_explorer",
                [_finding(e) for e in found["ai_explorer"]] if seeded and i != 3 else [],
            )
            ex = d / "explorer" / str(i)
            ex.mkdir(parents=True)
            status = "rate_limited" if i == 3 else "completed"
            (ex / "manifest.json").write_text(json.dumps(_explorer_manifest(i, status)), encoding="utf-8")
            (ex / "coverage.json").write_text(json.dumps(_explorer_coverage()), encoding="utf-8")

    for name, files in (("judge-stab", (2, 3)), ("explorer-stab", (1, 2)), ("explorer-stab-with-partial", (1, 2, 3))):
        d = root / name
        d.mkdir()
        prefix = "findings-ai-judge-" if name == "judge-stab" else "findings-ai-explorer-"
        for i in files:
            shutil.copy(root / "seeded" / f"{prefix}{i}.json", d / f"{prefix}{i}.json")
    return {"root": root}


def _args(root: Path, out: Path, explorer: bool, explorer_stability: str = "explorer-stab") -> list[str]:
    args = [
        "--det-seeded", str(root / "seeded" / "findings.json"),
        "--det-clean", str(root / "clean" / "findings.json"),
        "--ai-seeded", str(root / "seeded" / "findings-ai-judge-1.json"),
        "--ai-clean", str(root / "clean" / "findings-ai-judge-1.json"),
        "--ai-stability", str(root / "judge-stab"),
        "--out", str(out),
    ]
    if explorer:
        args += [
            "--explorer-seeded", str(root / "seeded" / "findings-ai-explorer-1.json"),
            "--explorer-clean", str(root / "clean" / "findings-ai-explorer-1.json"),
            "--explorer-stability", str(root / explorer_stability),
        ]
    return args


def test_two_approach_output_without_explorer_inputs(run_dir, tmp_path):
    out = tmp_path / "comparison.md"
    assert main(_args(run_dir["root"], out, explorer=False)) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# Phase 1 vs phase 2 comparison - run synthetic")
    assert "| id | category | expected_layer | deterministic | AI judge | union |" in text
    assert "explorer" not in text.lower()
    assert "## 4. Stability across the 2 AI judge repeats (seeded build)" in text
    assert "| **total** | | | **15/21** | **11/21** | **21/21** |" in text


def test_three_approach_output_with_explorer_inputs(run_dir, tmp_path):
    out = tmp_path / "comparison.md"
    assert main(_args(run_dir["root"], out, explorer=True)) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# Phase 1 vs phase 2 vs phase 3 comparison - run synthetic")
    assert "| id | category | expected_layer | deterministic | AI judge | AI explorer | union of all three |" in text
    assert "| **total** | | | **15/21** | **11/21** | **7/21** | **21/21** |" in text
    only_det = next(line for line in text.splitlines() if line.startswith("| deterministic | D0"))
    assert "D02" in only_det and "D01" not in only_det  # D01 is also found by the explorer
    assert "| none of the three | none |" in text
    assert "| AI explorer | 1/10 (10%) | 6/6 (100%) | 0/5 (0%) | 7/21 (33%) |" in text
    assert "AI explorer detected in (runs 1/2)" in text
    assert "| D01 | deterministic | 0/2 | no | 2/2 |" in text
    assert "### AI explorer: calls, tokens, notional cost, duration" in text
    assert "| seeded run 3 (excluded from stability) | rate_limited | 13 | 53 | 3 | 904 | 700 | 200 | 4 | 100 |" in text
    assert "| seeded run 1 (single run) | completed | 11 | 51 | 1 | 904 | 700 | 200 | 4 | 100 |" in text
    assert "| seeded run 1 (single run) | 4/5 | 5/5 | 6/10 | 8/10 |" in text


def test_partial_explorer_arguments_rejected(run_dir, tmp_path):
    args = _args(run_dir["root"], tmp_path / "comparison.md", explorer=True)
    i = args.index("--explorer-clean")
    del args[i:i + 2]
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert exc.value.code == 2


def test_rate_limited_run_rejected_from_explorer_stability(run_dir, tmp_path):
    args = _args(run_dir["root"], tmp_path / "comparison.md", explorer=True, explorer_stability="explorer-stab-with-partial")
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert "findings-ai-explorer-3.json" in str(exc.value)
    assert "rate_limited" in str(exc.value)
