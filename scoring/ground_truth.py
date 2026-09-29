"""Loads ground_truth/defects.yaml, ground_truth/controls.yaml, and
ground_truth/known_issues.yaml into the shape the matcher needs: paths
and testids pre-normalized."""
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ground_truth.pages import PAGE_PATHS
from scoring.normalize import normalize_path, normalize_testid

ROOT = Path(__file__).resolve().parent.parent
GROUND_TRUTH_DIR = ROOT / "ground_truth"


@dataclass(frozen=True)
class Entry:
    id: str
    category: str
    page_paths: tuple[str, ...]
    testids: tuple[str, ...]  # normalized, may be empty (no single element)
    fr_clean: str
    fr_seeded: str
    expected_layer: str | None  # None for controls


@dataclass(frozen=True)
class KnownIssue:
    id: str
    page_paths: tuple[str, ...]
    testids: tuple[str, ...]
    categories: tuple[str, ...]
    # Path-prefix issues (no single page or element, e.g. unknown URLs)
    # match testid-less findings on any path under one of these prefixes,
    # except the pages in excluded_page_paths (the real page map).
    page_path_prefixes: tuple[str, ...] = ()
    excluded_page_paths: tuple[str, ...] = ()


def _load_entries(filename: str, require_layer: bool) -> list[Entry]:
    raw = yaml.safe_load((GROUND_TRUTH_DIR / filename).read_text(encoding="utf-8")) or []
    entries = []
    for e in raw:
        page_paths = tuple(normalize_path(p) for p in PAGE_PATHS[e["page"]])
        testid = normalize_testid(e.get("data_testid"))
        also = [normalize_testid(t) for t in e.get("also_testids", [])]
        testids = tuple(t for t in [testid, *also] if t is not None)
        entries.append(
            Entry(
                id=e["id"],
                category=e["category"],
                page_paths=page_paths,
                testids=testids,
                fr_clean=e["fr_clean"],
                fr_seeded=e["fr_seeded"],
                expected_layer=e.get("expected_layer") if require_layer else None,
            )
        )
    return entries


def load_defects() -> list[Entry]:
    return _load_entries("defects.yaml", require_layer=True)


def load_controls() -> list[Entry]:
    return _load_entries("controls.yaml", require_layer=False)


def load_known_issues() -> list[KnownIssue]:
    raw = yaml.safe_load((GROUND_TRUTH_DIR / "known_issues.yaml").read_text(encoding="utf-8")) or []
    mapped_pages = tuple(normalize_path(p) for paths in PAGE_PATHS.values() for p in paths)
    issues = []
    for e in raw:
        page_paths = tuple(normalize_path(p) for p in e.get("page_paths", []))
        testids = tuple(t for t in (normalize_testid(t) for t in e.get("testids", [])) if t is not None)
        # Prefixes are not run through normalize_path, which would strip
        # the trailing slash and make "/fr/" also match "/frost".
        prefixes = tuple(p.lower() for p in e.get("page_path_prefixes", []))
        issues.append(
            KnownIssue(
                id=e["id"],
                page_paths=page_paths,
                testids=testids,
                categories=tuple(e["categories"]),
                page_path_prefixes=prefixes,
                excluded_page_paths=mapped_pages if prefixes else (),
            )
        )
    return issues


def controls_holding_in(controls: list[Entry], build: str) -> list[Entry]:
    """Controls whose value actually is the same in this build. Excludes
    e.g. C10 and C11, which only hold in the clean build (A06/A07 occupy
    the same elements in the seeded build)."""
    if build == "clean":
        return controls
    return [c for c in controls if c.fr_seeded == c.fr_clean]
