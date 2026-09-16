"""For each entry in ground_truth/defects.yaml: present in seeded mode,
absent (i.e. the clean value shows) in clean mode. Checked via the
element's data-testid, per entry's own detection method (text, an
attribute, the root html lang, or served image bytes)."""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFECTS = yaml.safe_load((ROOT / "ground_truth" / "defects.yaml").read_text(encoding="utf-8"))

DEMO_APP_ID = "AP-100482"

PAGE_PATH = {
    "landing": "/fr/",
    "calculator": "/fr/calculator",
    "apply": "/fr/apply",
    "summary": f"/fr/application/{DEMO_APP_ID}",
    "dashboard": "/fr/dashboard",
}


def _tag(page_html: str, testid: str) -> str:
    m = re.search(r'<[^>]*data-testid="%s"[^>]*>' % re.escape(testid), page_html)
    assert m, f"data-testid={testid!r} not found in page"
    return m.group(0)


def _text(page_html: str, testid: str) -> str:
    tag = _tag(page_html, testid)
    start = page_html.index(tag) + len(tag)
    end = page_html.index("<", start)
    return html_lib.unescape(page_html[start:end])


def _attr(page_html: str, testid: str, attr: str) -> str:
    tag = _tag(page_html, testid)
    m = re.search(r'%s="([^"]*)"' % re.escape(attr), tag)
    assert m, f"attribute {attr!r} not found on data-testid={testid!r}"
    return html_lib.unescape(m.group(1))


def _html_lang(page_html: str) -> str:
    m = re.search(r'<html lang="([^"]*)"', page_html)
    assert m
    return m.group(1)


def _check_text_defect(entry, page_html, expected):
    actual = _text(page_html, entry["data_testid"])
    assert actual == expected, f"{entry['id']}: expected {expected!r}, got {actual!r}"


def _check_d02_clean(entry, page_html, expected):
    # {amount} interpolates correctly in clean mode, so we can only check
    # the fixed prefix/suffix around the dynamic amount there.
    actual = _text(page_html, entry["data_testid"])
    prefix, suffix = re.match(r"^(.*?)\{amount\}(.*)$", expected).groups()
    assert actual.startswith(prefix) and actual.endswith(suffix), (entry["id"], actual)
    assert "{montant}" not in actual, f"{entry['id']}: unresolved placeholder leaked into clean mode: {actual!r}"


def _check_d02_seeded(entry, page_html):
    # In seeded mode the placeholder name is wrong (montant vs amount) and
    # stays fully literal, so we can assert the exact string.
    actual = _text(page_html, entry["data_testid"])
    assert actual == entry["fr_seeded"], (entry["id"], actual)


def _check_a05(entry, page_html, expected):
    actual = _text(page_html, entry["data_testid"])
    expected_text = expected.replace("{rate}", "5,2 %")
    assert actual == expected_text, f"{entry['id']}: expected {expected_text!r}, got {actual!r}"


def _check_d04(entry, page_html, should_be_clipped: bool):
    tag = _tag(page_html, entry["data_testid"])
    has_clip_class = "btn-compact" in tag
    assert has_clip_class == should_be_clipped, (
        f"{entry['id']}: expected clipping class present={should_be_clipped}, tag={tag!r}"
    )


def _check_d07(entry, page_html, expected):
    actual = _html_lang(page_html)
    assert actual == expected, f"{entry['id']}: html lang expected {expected!r}, got {actual!r}"


def _check_d08(entry, page_html, expected):
    actual = _attr(page_html, entry["data_testid"], "href")
    assert actual == expected, f"{entry['id']}: expected href {expected!r}, got {actual!r}"


def _check_image(entry, client, page_html, expected_path):
    src = _attr(page_html, entry["data_testid"], "src")
    assert src == expected_path, f"{entry['id']}: expected src {expected_path!r}, got {src!r}"
    served = client.get(src).get_data()
    on_disk = (ROOT / expected_path.lstrip("/")).read_bytes()
    assert served == on_disk, f"{entry['id']}: served image bytes differ from {expected_path}"


EMPTY_APPLY_FORM = {
    "full_name": "",
    "email": "",
    "phone": "",
    "amount": "",
    "term": "",
    "consent": "",
}


@pytest.mark.parametrize("entry", DEFECTS, ids=[e["id"] for e in DEFECTS])
def test_defect_present_in_seeded_absent_in_clean(entry, clean_client, seeded_client):
    defect_id = entry["id"]
    page_path = PAGE_PATH[entry["page"]]

    if defect_id == "D09":
        # Validation errors only render after a submission; GETting the
        # bare page never shows them.
        clean_html = clean_client.post(page_path, data=EMPTY_APPLY_FORM).get_data(as_text=True)
        seeded_html = seeded_client.post(page_path, data=EMPTY_APPLY_FORM).get_data(as_text=True)
        _check_text_defect(entry, clean_html, entry["fr_clean"])
        _check_text_defect(entry, seeded_html, entry["fr_seeded"])
        return

    clean_html = clean_client.get(page_path).get_data(as_text=True)
    seeded_html = seeded_client.get(page_path).get_data(as_text=True)

    if defect_id == "D04":
        _check_d04(entry, clean_html, should_be_clipped=False)
        _check_d04(entry, seeded_html, should_be_clipped=True)
    elif defect_id == "D02":
        _check_d02_clean(entry, clean_html, entry["fr_clean"])
        _check_d02_seeded(entry, seeded_html)
    elif defect_id == "A05":
        _check_a05(entry, clean_html, entry["fr_clean"])
        _check_a05(entry, seeded_html, entry["fr_seeded"])
    elif defect_id == "D07":
        _check_d07(entry, clean_html, entry["fr_clean"])
        _check_d07(entry, seeded_html, entry["fr_seeded"])
    elif defect_id == "D08":
        _check_d08(entry, clean_html, entry["fr_clean"])
        _check_d08(entry, seeded_html, entry["fr_seeded"])
    elif defect_id == "A06":
        _check_image(entry, clean_client, clean_html, entry["fr_clean"])
        _check_image(entry, seeded_client, seeded_html, entry["fr_seeded"])
    else:
        _check_text_defect(entry, clean_html, entry["fr_clean"])
        _check_text_defect(entry, seeded_html, entry["fr_seeded"])
