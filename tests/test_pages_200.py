import pytest

from tests.conftest import LOCALES, PAGE_PATHS

BUILD_MODES = ["clean", "seeded"]


@pytest.mark.parametrize("build", BUILD_MODES)
@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("page", list(PAGE_PATHS))
def test_page_returns_200(build, locale, page, both_clients):
    client = both_clients[build]
    path = PAGE_PATHS[page].format(lang=locale)
    resp = client.get(path)
    assert resp.status_code == 200, f"{build}/{locale}/{page} -> {resp.status_code}"


@pytest.mark.parametrize("build", BUILD_MODES)
def test_health(build, both_clients):
    resp = both_clients[build].get("/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "ok"
    assert body["build"] == build


@pytest.mark.parametrize("build", BUILD_MODES)
def test_root_redirect_by_accept_language(build, both_clients):
    client = both_clients[build]
    resp_fr = client.get("/", headers={"Accept-Language": "fr-CA,fr;q=0.9"})
    assert resp_fr.status_code in (301, 302, 303, 307, 308)
    assert resp_fr.headers["Location"].rstrip("/").endswith("/fr")

    resp_en = client.get("/", headers={"Accept-Language": "en-US,en;q=0.9"})
    assert resp_en.headers["Location"].rstrip("/").endswith("/en")


@pytest.mark.parametrize("build", BUILD_MODES)
@pytest.mark.parametrize("locale", LOCALES)
def test_apply_flow_reaches_summary(build, locale, both_clients):
    client = both_clients[build]
    data = {
        "full_name": "Jean Tremblay" if locale == "fr" else "John Smith",
        "email": "demo@example.com",
        "phone": "514-555-0100",
        "amount": "15000",
        "term": "36",
        "consent": "on",
    }
    resp = client.post(f"/{locale}/apply", data=data)
    assert resp.status_code in (301, 302, 303, 307, 308)
    location = resp.headers["Location"]
    summary_resp = client.get(location)
    assert summary_resp.status_code == 200
