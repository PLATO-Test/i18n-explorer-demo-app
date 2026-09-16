import pytest

from tests.conftest import PAGE_PATHS


@pytest.mark.parametrize("page", list(PAGE_PATHS))
def test_english_page_byte_identical_clean_vs_seeded(page, clean_client, seeded_client):
    path = PAGE_PATHS[page].format(lang="en")
    clean_bytes = clean_client.get(path).get_data()
    seeded_bytes = seeded_client.get(path).get_data()
    assert clean_bytes == seeded_bytes, f"English {page} differs between clean and seeded builds"
