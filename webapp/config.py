import datetime
import os
import zoneinfo

TIMEZONE = zoneinfo.ZoneInfo("America/Toronto")


def build_config(seeded: bool | None = None, app_today: str | None = None) -> dict:
    """Read config fresh on every call (never baked in at import time) so
    a single test process can build both a clean and a seeded app."""
    if seeded is None:
        seeded = os.environ.get("SEEDED_DEFECTS", "0") == "1"
    if app_today is None:
        app_today = os.environ.get("APP_TODAY", "2026-09-16")
    return {
        "SECRET_KEY": os.environ.get("SECRET_KEY", "dev-secret-key-not-for-production"),
        "SEEDED_DEFECTS": seeded,
        "APP_TODAY": datetime.date.fromisoformat(app_today),
        "BUILD_NAME": "seeded" if seeded else "clean",
    }
