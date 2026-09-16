"""Minimal i18next-style translation helper.

Behaviours (mirrors i18next so this reads like a real frontend stack ported
server-side, not a purpose-built test fixture):
  - a key missing in fr falls back to the en value
  - an unresolved {placeholder} renders literally
  - plural category is chosen from the CLDR rules of the active locale
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from babel import Locale

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent / "translations"

_PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")
_BABEL_LOCALE = {"en": "en_CA", "fr": "fr_CA"}


@lru_cache(maxsize=4)
def _load_json(path_str: str) -> dict:
    with open(path_str, encoding="utf-8") as fh:
        return json.load(fh)


def _load_en() -> dict:
    return _load_json(str(TRANSLATIONS_DIR / "en.json"))


def _load_fr_base() -> dict:
    return _load_json(str(TRANSLATIONS_DIR / "fr.json"))


def _load_fr_overrides() -> dict:
    return _load_json(str(TRANSLATIONS_DIR / "seeded" / "fr.overrides.json"))


def _deep_merge(base: dict, patch: dict) -> dict:
    out = dict(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _delete_path(tree: dict, dotted_key: str) -> None:
    parts = dotted_key.split(".")
    node = tree
    for part in parts[:-1]:
        node = node.get(part)
        if node is None:
            return
    node.pop(parts[-1], None)


def build_fr_catalog(seeded: bool) -> dict:
    catalog = json.loads(json.dumps(_load_fr_base()))  # deep copy
    if seeded:
        overrides = _load_fr_overrides()
        catalog = _deep_merge(catalog, overrides.get("overrides", {}))
        for dotted_key in overrides.get("delete", []):
            _delete_path(catalog, dotted_key)
    return catalog


def _lookup(tree: dict, dotted_key: str):
    node = tree
    for part in dotted_key.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _interpolate(template: str, params: dict) -> str:
    def repl(match: re.Match) -> str:
        name = match.group(1)
        if name in params:
            return str(params[name])
        return match.group(0)

    return _PLACEHOLDER_RE.sub(repl, template)


class Translator:
    """Bound to one request's locale (and, for fr, seeded state)."""

    def __init__(self, locale: str, seeded: bool):
        self.locale = locale
        self.seeded = seeded
        self._en = _load_en()
        self._active = self._en if locale == "en" else build_fr_catalog(seeded)

    def raw(self, key: str) -> str | None:
        value = _lookup(self._active, key)
        if value is None:
            value = _lookup(self._en, key)  # i18next-style fallback to en
        return value

    def t(self, key: str, count: int | None = None, plural_locale: str | None = None, **params) -> str:
        lookup_key = key
        if count is not None:
            babel_locale = _BABEL_LOCALE[plural_locale or self.locale]
            category = Locale.parse(babel_locale).plural_form(count)
            lookup_key = f"{key}_{category}"
            params = {**params, "count": count}
        value = self.raw(lookup_key)
        if value is None:
            return f"{{{lookup_key}}}"
        return _interpolate(value, params)
