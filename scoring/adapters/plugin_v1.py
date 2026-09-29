"""Converts an i18n-explorer plugin findings.json (plugin findings schema
1.x) into the scorer's input format. The source file is only read.

    uv run python -m scoring.adapters.plugin_v1 <plugin findings.json> <output .json>

Mapping rules, per finding:

- page_path: the path of the URL for the finding's locale (fr_url when
  locale is "fr", en_url when "en"), without host, query string or
  fragment. Case and trailing slashes are left to the scorer's own
  normalize_path.
- data_testid: `element` when it looks like a data-testid - a non-empty
  string with no whitespace, quote characters, brackets or "=". Some runs
  instead copy the plugin's own read_page notation, `[testid=X]`, or
  write it without brackets, `testid=X`, either optionally after a role
  (`img [testid=X]`); X is taken from that when it is the only testid in
  `element`. The plugin's other form, a role plus accessible name
  (`button "Envoyer"`), and any element naming several testids (`a / b`,
  `[testid=a] / [testid=b]`) become null.
- observed: fr_text or en_text, by locale. Missing or empty is an error:
  the scorer requires a non-empty observed value.
- expected: suggested_fix.
- category: copied unchanged when the scorer knows it (both schemas use
  the same 16 names). Any other category is an error, listed by finding
  id; it is never coerced to "other", since the matcher uses category for
  some matches.
- description, severity: copied unchanged.
- evidence: the first entry of the plugin's evidence list (its latest
  screenshot of the page if there is one, else the trajectory entry), or
  null.

Run block: run_id, base_url, started_at and duration_s are copied, model
is model_configured, source is "ai_explorer". The plugin records no token
counts or cost, so those are null.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent.parent
SCORER_SCHEMA_PATH = ROOT / "scoring" / "findings.schema.json"

_TESTID_RE = re.compile(r"""^[^\s"'‘’“”\[\]=]+$""")
_BRACKETED_TESTID_RE = re.compile(r"""^(?:[a-z]+\s+)?(?:\[testid=([^\s"'‘’“”\[\]=]+)\]|testid=([^\s"'‘’“”\[\]=]+))$""")


class UnknownCategoryError(ValueError):
    """One or more findings use a category the scorer does not know.
    `unknown` maps finding id -> category."""

    def __init__(self, unknown: dict[str, str]):
        self.unknown = unknown
        listed = ", ".join(f"{fid}: {cat}" for fid, cat in unknown.items())
        super().__init__(f"categories the scorer does not know: {listed}")


def scorer_categories() -> set[str]:
    schema = json.loads(SCORER_SCHEMA_PATH.read_text(encoding="utf-8"))
    return set(schema["$defs"]["finding"]["properties"]["category"]["enum"])


def looks_like_testid(element: str | None) -> bool:
    return bool(element) and _TESTID_RE.match(element) is not None


def element_testid(element: str | None) -> str | None:
    if looks_like_testid(element):
        return element
    m = _BRACKETED_TESTID_RE.match(element or "")
    return (m.group(1) or m.group(2)) if m else None


def _convert_finding(f: dict) -> dict:
    locale = f["locale"]
    if locale not in ("fr", "en"):
        raise ValueError(f"{f.get('id')}: unknown locale {locale!r}")
    url = f[f"{locale}_url"]
    observed = f[f"{locale}_text"]
    if not url:
        raise ValueError(f"{f.get('id')}: {locale}_url is empty for a {locale} finding")
    if not observed:
        raise ValueError(f"{f.get('id')}: {locale}_text is empty for a {locale} finding")
    evidence = f.get("evidence") or []
    return {
        "page_path": urlsplit(url).path or "/",
        "data_testid": element_testid(f.get("element")),
        "category": f["category"],
        "observed": observed,
        "expected": f.get("suggested_fix"),
        "description": f["description"],
        "severity": f["severity"],
        "evidence": evidence[0] if evidence else None,
    }


def convert(doc: dict) -> dict:
    """Returns a new scorer-format document; `doc` is not modified."""
    known = scorer_categories()
    unknown = {f.get("id", f"#{i}"): f["category"] for i, f in enumerate(doc["findings"]) if f["category"] not in known}
    if unknown:
        raise UnknownCategoryError(unknown)
    run = doc["run"]
    return {
        "run": {
            "run_id": run["run_id"],
            "source": "ai_explorer",
            "base_url": run["base_url"],
            "started_at": run["started_at"],
            "model": run.get("model_configured"),
            "input_tokens": None,
            "output_tokens": None,
            "cost_usd": None,
            "duration_s": run["duration_s"],
        },
        "findings": [_convert_finding(f) for f in doc["findings"]],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert an i18n-explorer plugin findings.json to the scorer's format.")
    parser.add_argument("source", type=Path, help="Plugin findings.json (read only).")
    parser.add_argument("out", type=Path, help="Output file in the scorer's format.")
    args = parser.parse_args(argv)

    if args.out.resolve() == args.source.resolve():
        print("refusing to overwrite the source file", file=sys.stderr)
        return 1
    doc = json.loads(args.source.read_text(encoding="utf-8"))
    try:
        converted = convert(doc)
    except UnknownCategoryError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(converted, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(converted['findings'])} findings to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
