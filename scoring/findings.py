"""Loads and validates findings files against scoring/findings.schema.json."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import jsonschema

from scoring.normalize import normalize_path, normalize_testid

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "scoring" / "findings.schema.json"


class FindingsValidationError(Exception):
    """One or more findings files failed schema validation. `errors` maps
    file path -> list of human-readable problems."""

    def __init__(self, errors: dict[Path, list[str]]):
        self.errors = errors
        summary = "\n".join(
            f"{path}:\n  " + "\n  ".join(msgs) for path, msgs in errors.items()
        )
        super().__init__(f"{len(errors)} findings file(s) failed schema validation:\n{summary}")


@dataclass(frozen=True)
class Finding:
    page_path: str  # normalized
    data_testid: str | None  # normalized
    category: str
    observed: str
    expected: str | None
    description: str
    severity: str
    evidence: str | None


@dataclass(frozen=True)
class Run:
    run_id: str
    source: str
    base_url: str
    started_at: str
    model: str | None
    input_tokens: int | None
    output_tokens: int | None
    cost_usd: float | None
    duration_s: float
    findings: list[Finding]
    file_path: Path


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def discover_files(findings_path: Path) -> list[Path]:
    if findings_path.is_dir():
        return sorted(findings_path.glob("*.json"))
    return [findings_path]


def validate_files(paths: list[Path]) -> None:
    """Validates every file, collecting all failures before raising, so a
    caller never sees a partial pass/fail picture."""
    schema = _load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    errors: dict[Path, list[str]] = {}
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors[path] = [f"invalid JSON: {exc}"]
            continue
        problems = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if problems:
            errors[path] = [
                f"{'/'.join(str(p) for p in problem.path) or '<root>'}: {problem.message}"
                for problem in problems
            ]
    if errors:
        raise FindingsValidationError(errors)


def _load_run(path: Path) -> Run:
    data = json.loads(path.read_text(encoding="utf-8"))
    run = data["run"]
    findings = [
        Finding(
            page_path=normalize_path(f["page_path"]),
            data_testid=normalize_testid(f["data_testid"]),
            category=f["category"],
            observed=f["observed"],
            expected=f["expected"],
            description=f["description"],
            severity=f["severity"],
            evidence=f["evidence"],
        )
        for f in data["findings"]
    ]
    return Run(
        run_id=run["run_id"],
        source=run["source"],
        base_url=run["base_url"],
        started_at=run["started_at"],
        model=run["model"],
        input_tokens=run["input_tokens"],
        output_tokens=run["output_tokens"],
        cost_usd=run["cost_usd"],
        duration_s=run["duration_s"],
        findings=findings,
        file_path=path,
    )


def load_runs(findings_path: Path) -> list[Run]:
    """Validates every discovered file first (raising on any failure), then
    loads and returns all of them - never scores a partial set."""
    paths = discover_files(findings_path)
    validate_files(paths)
    return [_load_run(p) for p in paths]
