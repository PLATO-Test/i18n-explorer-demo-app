"""Babel-backed formatting helpers. Every formatted number, currency, or
date the app renders comes from one of these — never hand-typed."""
from __future__ import annotations

import datetime

from babel.dates import format_date
from babel.numbers import format_currency, format_percent

BABEL_LOCALE = {"en": "en_CA", "fr": "fr_CA"}

_PERCENT_PATTERN = {
    "en": "#,##0.0%",
    "fr": "#,##0.0 %",
}


def money(amount: float, locale: str, force_locale: str | None = None) -> str:
    babel_locale = force_locale or BABEL_LOCALE[locale]
    return format_currency(amount, "CAD", locale=babel_locale)


def percent(value: float, locale: str) -> str:
    return format_percent(value, locale=BABEL_LOCALE[locale], format=_PERCENT_PATTERN[locale])


def date_long(d: datetime.date, locale: str) -> str:
    return format_date(d, format="long", locale=BABEL_LOCALE[locale])


def date_short(d: datetime.date, locale: str, force_mmddyyyy: bool = False) -> str:
    if force_mmddyyyy:
        return format_date(d, format="MM/dd/yyyy", locale="en_US")
    return format_date(d, format="short", locale=BABEL_LOCALE[locale])
