"""For each entry in ground_truth/controls.yaml, the expected fr-CA text
is present in both build modes (these must never be flagged as defects).
C10 and C11 are the documented exceptions: they only hold in clean mode,
since in seeded mode those same locations show the A06/A07 defects by
design."""
import html as html_lib
import re
from pathlib import Path

import pytest
import yaml

from tests.conftest import DEMO_APP_ID

ROOT = Path(__file__).resolve().parent.parent
CONTROLS = yaml.safe_load((ROOT / "ground_truth" / "controls.yaml").read_text(encoding="utf-8"))

PAGE_PATH = {
    "landing": "/fr/",
    "calculator": "/fr/calculator",
    "apply": "/fr/apply",
    "summary": f"/fr/application/{DEMO_APP_ID}",
    "dashboard": "/fr/dashboard",
    "header": "/fr/",
}


def _tag(html: str, testid: str) -> str:
    m = re.search(r'<[^>]*data-testid="%s"[^>]*>' % re.escape(testid), html)
    assert m, f"data-testid={testid!r} not found in page"
    return m.group(0)


def _text(html: str, testid: str) -> str:
    tag = _tag(html, testid)
    start = html.index(tag) + len(tag)
    end = html.index("<", start)
    return html_lib.unescape(html[start:end])


def _attr(html: str, testid: str, attr: str) -> str:
    tag = _tag(html, testid)
    m = re.search(r'%s="([^"]*)"' % re.escape(attr), tag)
    assert m
    return html_lib.unescape(m.group(1))


IMAGE_CONTROLS = ("C10", "C11")


@pytest.mark.parametrize("entry", CONTROLS, ids=[e["id"] for e in CONTROLS])
def test_control_present_in_clean(entry, clean_client):
    html = clean_client.get(PAGE_PATH[entry["page"]]).get_data(as_text=True)
    if entry["id"] in IMAGE_CONTROLS:
        actual = _attr(html, entry["data_testid"], "src")
        expected = entry["fr_clean"] if entry["id"] == "C10" else f"/static/img/{entry['fr_clean_image']}"
    else:
        actual = _text(html, entry["data_testid"])
        expected = entry["fr_clean"]
    assert actual == expected, f"{entry['id']}: expected {expected!r}, got {actual!r}"


@pytest.mark.parametrize(
    "entry",
    [e for e in CONTROLS if e["id"] not in IMAGE_CONTROLS],
    ids=[e["id"] for e in CONTROLS if e["id"] not in IMAGE_CONTROLS],
)
def test_control_present_in_seeded(entry, seeded_client):
    html = seeded_client.get(PAGE_PATH[entry["page"]]).get_data(as_text=True)
    actual = _text(html, entry["data_testid"])
    assert actual == entry["fr_seeded"], f"{entry['id']}: expected {entry['fr_seeded']!r}, got {actual!r}"
