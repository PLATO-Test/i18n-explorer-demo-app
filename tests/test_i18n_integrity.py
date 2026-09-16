import json
import re
from pathlib import Path

import pytest

from tests.conftest import LOCALES, PAGE_PATHS

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent / "translations"

PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z_]\w*\}")


def _flatten_keys(tree: dict, prefix: str = "") -> set[str]:
    keys = set()
    for k, v in tree.items():
        dotted = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys |= _flatten_keys(v, dotted)
        else:
            keys.add(dotted)
    return keys


def test_en_fr_key_sets_match_in_clean_mode():
    en = json.loads((TRANSLATIONS_DIR / "en.json").read_text(encoding="utf-8"))
    fr = json.loads((TRANSLATIONS_DIR / "fr.json").read_text(encoding="utf-8"))
    en_keys = _flatten_keys(en)
    fr_keys = _flatten_keys(fr)
    assert en_keys == fr_keys, f"key mismatch: only-en={en_keys - fr_keys} only-fr={fr_keys - en_keys}"


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("page", list(PAGE_PATHS))
def test_no_unresolved_placeholders_clean_mode(locale, page, clean_client):
    path = PAGE_PATHS[page].format(lang=locale)
    html = clean_client.get(path).get_data(as_text=True)
    matches = PLACEHOLDER_RE.findall(html)
    assert not matches, f"{locale}/{page} has unresolved placeholders: {matches}"


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("page", list(PAGE_PATHS))
def test_html_lang_correct_clean_mode(locale, page, clean_client):
    path = PAGE_PATHS[page].format(lang=locale)
    html = clean_client.get(path).get_data(as_text=True)
    expected = "fr-CA" if locale == "fr" else "en"
    match = re.search(r'<html lang="([^"]*)"', html)
    assert match is not None
    assert match.group(1) == expected
