"""Page name -> fr page path(s), shared by the self-verification tests and
the scorer. All seeded/control entries live only on the French pages, so
these are fr-only. "header" renders on every page, hence the list."""

DEMO_APPLICATION_ID = "AP-100482"

PAGE_PATHS: dict[str, list[str]] = {
    "landing": ["/fr/"],
    "calculator": ["/fr/calculator"],
    "apply": ["/fr/apply"],
    "summary": [f"/fr/application/{DEMO_APPLICATION_ID}"],
    "dashboard": ["/fr/dashboard"],
    "header": [
        "/fr/",
        "/fr/calculator",
        "/fr/apply",
        f"/fr/application/{DEMO_APPLICATION_ID}",
        "/fr/dashboard",
    ],
}
