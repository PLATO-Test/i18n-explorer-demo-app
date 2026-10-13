# CLAUDE.md

## About this repo

Northstar Bank is a small demo bank website in English and French (fr-CA).
It has i18n defects that were added on purpose. We use it as a test target
for the i18n-explorer plugin: https://github.com/PLATO-Test/i18n-explorer

The app runs as two builds:

| Build  | Port | `SEEDED_DEFECTS` |
|--------|------|------------------|
| clean  | 5001 | `0`              |
| seeded | 5002 | `1`              |

Main folders:

- `webapp/` – the Flask app.
- `translations/` – English and French texts. The wrong French texts for
  the seeded build are in `translations/seeded/fr.overrides.json`.
- `ground_truth/` – the list of defects (the answer key).
- `scoring/` – compares a findings report with the answer key.
- `tests/` – pytest tests for the app and the scorer.

## Keep the answer key secret

The tool under test must find defects only by looking at the website.

- Do not show defects in the page. No words like "defect", "seeded", "bug"
  and no defect IDs in HTML, CSS class names, comments, `data-testid`
  values or HTTP responses.
- Defects must look like normal mistakes of a developer or translator.
- Never run the tool under test from this folder. It would read this file
  and `ground_truth/`.
- `ground_truth/`, `tests/scoring_fixtures/` and scorer reports contain the
  answers. Do not give them to the tool under test.
- Scorer reports go only to the `out/` folder (it is in `.gitignore`).
- `scoring/findings.schema.json` must not contain real pages, testids or
  texts from `ground_truth/`.
- `README.md` must not describe individual defects.

## Rules for changes

1. Show proof. Before you say that something works, run the command
   (server, `curl`, `pytest`) and show the output.
2. English pages must be the same in both builds, byte for byte. Turn a
   defect on only when the build is seeded AND the language is French.
3. Do not type French numbers, money or dates by hand. Use
   `webapp/formatting.py` (Babel). Keep the special spaces (U+00A0) that
   Babel adds.
4. French texts use Quebec banking terms and "vous". If you are not sure
   about a French text, add a note to `TRANSLATION_NOTES.md`.
5. Use the simple apostrophe `'`, not `’`.
6. Files use LF line endings.

## How to run

`README.md` explains how to start the app (locally and with Docker), how
to run the tests, and what can go wrong. Read it before you start a server
or Docker. In short:

- Use uv: `uv sync`, `uv run pytest`, `uv run flask ...`. Do not use `pip`
  or `python` directly.
- Use `docker compose`, not `docker-compose`.
- Dates are fixed on purpose: "today" is 2026-09-16 (`APP_TODAY`).

## Code notes

- `webapp/i18n.py`: if a French key is missing, the English text is shown.
- `static/` is in the project root, not in `webapp/`. This is why
  `create_app()` sets `static_folder`.
- `ground_truth/pages.py`: the only place that maps page names to URLs.
- `scoring/adapters/plugin_v1.py`: converts an i18n-explorer report to the
  scorer format.
- `scoring/matcher.py`: checks each finding against defects first, then
  known issues, then controls. Read `FALLBACK_OVERRIDES` there before you
  change D07 or A06 in `ground_truth/defects.yaml`.
