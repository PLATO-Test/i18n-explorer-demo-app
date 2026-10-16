"""Tests for scoring.adapters.plugin_v1, using inline synthetic plugin
findings documents."""
import copy
import json

import jsonschema
import pytest

from scoring.adapters.plugin_v1 import (
    SCORER_SCHEMA_PATH,
    UnknownCategoryError,
    convert,
    looks_like_testid,
    main,
)


def _finding(**overrides) -> dict:
    f = {
        "id": "F001",
        "category": "missing_translation",
        "severity": "medium",
        "locale": "fr",
        "fr_url": "http://localhost:9999/fr/somewhere",
        "en_url": "http://localhost:9999/en/somewhere",
        "element": "some-widget",
        "fr_text": "Texte observé",
        "en_text": "Observed text",
        "suggested_fix": "Texte corrigé",
        "description": "Something is wrong.",
        "evidence": ["screenshots/001.png", "trajectory.jsonl#seq=3"],
    }
    f.update(overrides)
    return f


def _doc(*findings) -> dict:
    return {
        "run": {
            "schema_version": "1.0.0",
            "run_id": "20260101-000000-localhost-9999",
            "plugin_version": "0.1.0",
            "model_configured": "some-model",
            "base_url": "http://localhost:9999",
            "started_at": "2026-01-01T00:00:00-05:00",
            "finished_at": "2026-01-01T00:02:00-05:00",
            "duration_s": 120.5,
            "status": "completed",
            "limits": {"max_tool_calls": 120, "max_screenshots": 20, "max_minutes": 25.0},
            "budget_used": {"tool_calls": 10, "screenshots": 1, "minutes": 2.0, "exhausted": None},
            "finish_summary": "done",
        },
        "findings": list(findings),
    }


def _validate(converted: dict) -> None:
    schema = json.loads(SCORER_SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(converted)


def test_fr_finding_maps_every_field():
    out = convert(_doc(_finding()))
    assert out["findings"] == [
        {
            "page_path": "/fr/somewhere",
            "data_testid": "some-widget",
            "category": "missing_translation",
            "observed": "Texte observé",
            "expected": "Texte corrigé",
            "description": "Something is wrong.",
            "severity": "medium",
            "evidence": "screenshots/001.png",
        }
    ]
    _validate(out)


def test_en_finding_uses_en_url_and_en_text():
    f = _finding(locale="en", fr_url=None, fr_text=None, en_url="http://localhost:9999/en/other")
    [out] = convert(_doc(f))["findings"]
    assert out["page_path"] == "/en/other"
    assert out["observed"] == "Observed text"


def test_query_string_and_fragment_are_dropped():
    f = _finding(fr_url="http://localhost:9999/fr/page?x=1&y=2#section")
    assert convert(_doc(f))["findings"][0]["page_path"] == "/fr/page"


def test_bare_host_url_gives_root_path():
    f = _finding(fr_url="http://localhost:9999")
    assert convert(_doc(f))["findings"][0]["page_path"] == "/"


@pytest.mark.parametrize(
    "element, expected",
    [
        ("some-widget", "some-widget"),
        ("widget_2", "widget_2"),
        ('button "Envoyer"', None),
        ("link 'Suivant'", None),
        ("heading", "heading"),
        ("html", None),
        ("HTML", None),
        ("body", None),
        ("button", None),
        ("h1", None),
        ("", None),
        (None, None),
    ],
)
def test_element_becomes_testid_only_when_it_looks_like_one(element, expected):
    [out] = convert(_doc(_finding(element=element)))["findings"]
    assert out["data_testid"] == expected
    assert looks_like_testid(element) is (expected is not None)


@pytest.mark.parametrize(
    "element, expected",
    [
        ("[testid=some-widget]", "some-widget"),
        ("img [testid=some-widget]", "some-widget"),
        ("testid=some-widget", "some-widget"),
        ("img testid=some-widget", "some-widget"),
        ("[testid=a] / [testid=b]", None),
        ("testid=a / testid=b", None),
        ("[testid=some-widget", None),
        ("testid=some-widget]", None),
        ("a / b", None),
        ("[testid=]", None),
        ('button "Envoyer" [testid=some-widget]', None),
    ],
)
def test_bracketed_testid_is_unwrapped_only_when_it_is_the_only_one(element, expected):
    [out] = convert(_doc(_finding(element=element)))["findings"]
    assert out["data_testid"] == expected
    assert not looks_like_testid(element)


def test_evidence_takes_first_entry_or_null():
    [a, b] = convert(
        _doc(
            _finding(evidence=["trajectory.jsonl#seq=7"]),
            _finding(id="F002", evidence=[]),
        )
    )["findings"]
    assert a["evidence"] == "trajectory.jsonl#seq=7"
    assert b["evidence"] is None


def test_null_suggested_fix_gives_null_expected():
    [out] = convert(_doc(_finding(suggested_fix=None)))["findings"]
    assert out["expected"] is None


def test_missing_text_for_locale_is_an_error():
    with pytest.raises(ValueError, match="fr_text"):
        convert(_doc(_finding(fr_text=None)))


def test_unknown_category_is_reported_not_coerced():
    doc = _doc(_finding(), _finding(id="F002", category="layout"), _finding(id="F003", category="tone"))
    with pytest.raises(UnknownCategoryError) as excinfo:
        convert(doc)
    assert excinfo.value.unknown == {"F002": "layout", "F003": "tone"}


def test_run_block():
    out = convert(_doc(_finding()))
    assert out["run"] == {
        "run_id": "20260101-000000-localhost-9999",
        "source": "ai_explorer",
        "base_url": "http://localhost:9999",
        "started_at": "2026-01-01T00:00:00-05:00",
        "model": "some-model",
        "input_tokens": None,
        "output_tokens": None,
        "cost_usd": None,
        "duration_s": 120.5,
    }


def test_input_document_is_not_modified():
    doc = _doc(_finding(), _finding(id="F002", element='button "OK"', evidence=[]))
    before = copy.deepcopy(doc)
    convert(doc)
    assert doc == before


def test_cli_writes_output_and_leaves_source_unchanged(tmp_path):
    src = tmp_path / "findings.json"
    src.write_text(json.dumps(_doc(_finding())), encoding="utf-8")
    before = src.read_bytes()
    out = tmp_path / "out" / "converted.json"
    assert main([str(src), str(out)]) == 0
    assert src.read_bytes() == before
    _validate(json.loads(out.read_text(encoding="utf-8")))


def test_cli_refuses_to_overwrite_source(tmp_path):
    src = tmp_path / "findings.json"
    src.write_text(json.dumps(_doc(_finding())), encoding="utf-8")
    assert main([str(src), str(src)]) == 1


def test_cli_fails_on_unknown_category(tmp_path, capsys):
    src = tmp_path / "findings.json"
    src.write_text(json.dumps(_doc(_finding(category="layout"))), encoding="utf-8")
    assert main([str(src), str(tmp_path / "out.json")]) == 1
    assert "F001: layout" in capsys.readouterr().err
