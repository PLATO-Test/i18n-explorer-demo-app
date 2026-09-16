"""Test fixtures supporting two run modes:

- default: an in-process Flask app per build (webapp.app.create_app),
  exercised via Flask's own test client.
- against running containers: set APP_BASE_URL_CLEAN and/or
  APP_BASE_URL_SEEDED (e.g. http://localhost:5001 / :5002) and the same
  tests run real HTTP requests against them instead.

Client fixtures are function-scoped on purpose: several tests POST to
/apply and rely on session state, and a shared session-scoped client
would leak that state between unrelated tests.
"""
import os

import pytest
import requests

from webapp.app import create_app


class _HttpResponse:
    def __init__(self, r: requests.Response):
        self._r = r
        self.status_code = r.status_code
        self.headers = r.headers

    def get_data(self, as_text: bool = False):
        return self._r.text if as_text else self._r.content

    def get_json(self):
        return self._r.json()


class HttpClient:
    """Minimal adapter giving requests.Session() the same call shape as
    Flask's test client, for the subset this test suite uses."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get(self, path: str, follow_redirects: bool = False, **kwargs) -> _HttpResponse:
        r = self.session.get(self.base_url + path, allow_redirects=follow_redirects, **kwargs)
        return _HttpResponse(r)

    def post(self, path: str, data=None, follow_redirects: bool = False, **kwargs) -> _HttpResponse:
        r = self.session.post(self.base_url + path, data=data, allow_redirects=follow_redirects, **kwargs)
        return _HttpResponse(r)


def _make_client(base_url_env: str, seeded: bool):
    base = os.environ.get(base_url_env)
    if base:
        return HttpClient(base)
    app = create_app(seeded=seeded)
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def clean_client():
    return _make_client("APP_BASE_URL_CLEAN", seeded=False)


@pytest.fixture
def seeded_client():
    return _make_client("APP_BASE_URL_SEEDED", seeded=True)


@pytest.fixture
def both_clients(clean_client, seeded_client):
    return {"clean": clean_client, "seeded": seeded_client}


LOCALES = ["en", "fr"]

DEMO_APP_ID = "AP-100482"

PAGE_PATHS = {
    "landing": "/{lang}/",
    "calculator": "/{lang}/calculator",
    "apply": "/{lang}/apply",
    "summary": "/{lang}/application/" + DEMO_APP_ID,
    "dashboard": "/{lang}/dashboard",
}
