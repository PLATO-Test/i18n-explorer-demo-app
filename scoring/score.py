"""Scorer CLI: compares findings from a test run against this repo's
ground truth.

    uv run python -m scoring.score --findings <file-or-folder> --build seeded|clean --out <folder>

Reports (report.json, report.md) contain defect IDs and ground-truth text.
Keep them away from the tool under test - see CLAUDE.md.
"""
import argparse
import json
import sys
from pathlib import Path

from scoring.findings import FindingsValidationError, load_runs
from scoring.ground_truth import load_controls, load_defects, load_known_issues
from scoring.report import build_report, render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score i18n test findings against ground truth.")
    parser.add_argument("--findings", required=True, type=Path, help="A findings JSON file, or a folder of them.")
    parser.add_argument("--build", required=True, choices=["seeded", "clean"])
    parser.add_argument("--out", required=True, type=Path, help="Output folder for report.json / report.md.")
    args = parser.parse_args(argv)

    try:
        runs = load_runs(args.findings)
    except FindingsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not runs:
        print(f"No findings files found at {args.findings}", file=sys.stderr)
        return 1

    defects = load_defects()
    controls = load_controls()
    known_issues = load_known_issues()
    report = build_report(runs, defects, controls, args.build, known_issues)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.out / "report.md").write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {args.out / 'report.json'} and {args.out / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
