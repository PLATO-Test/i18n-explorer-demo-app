"""Normalization helpers shared by ground-truth loading and finding
matching, so both sides of a comparison go through the same function."""
from __future__ import annotations

import unicodedata


def normalize_path(path: str) -> str:
    """Lowercase, drop query/fragment, strip a trailing slash (unless that
    would leave an empty string). '/fr/' and '/fr' both become '/fr'."""
    path = path.strip().split("?", 1)[0].split("#", 1)[0].lower()
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    return path


def normalize_testid(testid: str | None) -> str | None:
    """Treat '' the same as null - some producers write one, some the
    other, and ground truth (D07) also uses '' for "no single element"."""
    if testid is None or testid == "":
        return None
    return testid


def normalize_text(text: str) -> str:
    """Case-fold, collapse whitespace, and normalize to Unicode NFC so
    substring containment checks aren't defeated by incidental formatting
    differences between what a producer captured and the ground truth."""
    text = unicodedata.normalize("NFC", text)
    text = " ".join(text.split())
    return text.casefold()
