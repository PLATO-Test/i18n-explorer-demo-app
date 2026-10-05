# CLAUDE.md

Guidance for working on this repo.

## What this repo is

This is the **target application** for a proof of concept on AI-assisted
i18n testing. It is a bilingual (en / fr-CA) demo bank app
("Northstar Bank" / "Banque Northstar") with a catalog of deliberately
seeded i18n defects.

A **separate repo**, built independently, contains the AI test suite that
exercises this app. That test suite, and any AI judge it drives, must
**never** see this repo's source code or its defect manifest
(`ground_truth/`). Keep that boundary in mind for anything written here:
rendered HTML, CSS class names, HTML comments, `data-testid` values, and
HTTP responses must never reveal that a defect exists — no words like
"defect", "seeded", "bug", "broken", or defect IDs anywhere in rendered
output. Seeded defects must look like realistic developer or translator
mistakes, not like obvious test fixtures.

## Environment facts

- The project lives on **Windows**. Claude Code runs natively on Windows
  here (not inside WSL).
- Docker Engine is **not** installed on Windows — it runs inside **WSL2
  Ubuntu** (distro name `Ubuntu`) and must be invoked from Windows
  through `wsl.exe`: `wsl -d Ubuntu -- docker ...` /
  `wsl -d Ubuntu -- docker compose ...` (Compose v2 plugin syntax; never
  `docker-compose`). Run these from the project root — `wsl.exe` maps the
  current Windows directory to its `/mnt/<drive>/...` equivalent.
- If Git Bash mangles path arguments to `wsl.exe`, prefix with
  `MSYS_NO_PATHCONV=1` or use relative paths only.
- Python tooling is `uv` with Python 3.14 (`requires-python =
  ">=3.14,<3.15"`). Use `uv sync`, `uv run pytest`, `uv run flask ...` —
  never a bare `pip`/`python` outside `uv run`.
- Ports 5001 (clean build) and 5002 (seeded build) are published by
  Docker inside WSL2 and must be reachable from Windows at
  `http://localhost:5001` / `:5002`.
- Timezone is `America/Toronto`, set explicitly (containers do not
  inherit the host timezone). "Today" is fixed via `APP_TODAY` (default
  `2026-09-16`) so all output is reproducible — there is no randomness
  anywhere in this app.
- Line endings: `.gitattributes` enforces `* text=auto eol=lf`. Every
  shell script, Dockerfile, and entrypoint must use LF, since they
  execute inside Linux containers. `.gitattributes` normalizes what git
  stores, not bytes already on disk — after editing such a file, verify
  with `git ls-files --eol` if in doubt.

## Ground rules for this codebase

- **Every claim that something works must be backed by a command actually
  run and shown** — server start, `curl`, `pytest` output. Don't assert
  success without having run the check.
- **No defect leakage into rendered output.** Rendered HTML, CSS class
  names, HTML comments, `data-testid` values, and HTTP responses must
  never reveal that a defect exists (see above). The defect manifest
  lives only in `ground_truth/defects.yaml` and `ground_truth/controls.yaml`.
  `README.md` must not describe individual defects.
- **Seeded defects must read as realistic mistakes** a developer or
  translator could plausibly make — not as obviously-planted test
  fixtures. Comments near seeded-defect code, if any, should read like a
  real (if slightly careless) developer note, never name the mechanism as
  a "defect" or "seed".
- **Never hand-type formatted numbers, currencies, or dates for fr-CA.**
  Generate them with Babel and use its output as-is, including its exact
  Unicode space characters (Babel's fr_CA output uses U+00A0 NBSP as a
  thousands separator and before currency/percent signs — don't
  normalize this to a regular space).
- **French text must follow Quebec / fr-CA financial terminology (OQLF
  conventions)** and address the reader with "vous" consistently (except
  where a seeded defect deliberately breaks this). Any French string
  you're not fully confident about goes in `TRANSLATION_NOTES.md` for
  human review — don't silently guess.
- Apostrophes: use `'` (U+0027) consistently across translations, YAML,
  templates, and tests — not the typographic `'` (U+2019). A mismatch
  breaks substring assertions in ways that look like translation bugs.
- English pages must render **byte-identical** between the clean and
  seeded builds (excluding nothing else — there are no CSRF tokens in
  this app). Any per-locale defect toggle must be gated on
  `seeded AND locale == 'fr'`, never on `seeded` alone, or English output
  will silently diverge between builds.

### Scoring / findings boundary

A separate repo holds the AI test suite (deterministic Playwright checks,
an AI judge, an AI explorer agent) that exercises this app and emits
findings in the shared format defined by `scoring/findings.schema.json`.
The scorer that grades those findings against ground truth lives here,
in `scoring/`, because it needs to read `ground_truth/`.

- **The only file allowed to leave this repo for the test repo is
  `scoring/findings.schema.json`.** It must never contain an embedded
  example, default, or comment that names a real page, testid, or string
  from `ground_truth/`.
- Scorer output (`report.json`, `report.md`) contains defect IDs and
  ground-truth text. Never copy it into the test repo, paste it into a
  prompt for an AI judge/explorer, or commit it to a location that repo
  might read from.
- `tests/scoring_fixtures/` holds synthetic findings used to test the
  scorer itself. These fixtures reference real defect testids/text to
  exercise the matcher meaningfully, so treat them the same as
  `ground_truth/` — they must not leave this repo either.

## Architecture notes worth knowing

- `webapp/i18n.py`: minimal i18next-style `Translator`. A key missing
  from `fr.json` falls back to the `en.json` value. An unresolved
  `{placeholder}` renders literally. Plural category comes from Babel's
  CLDR plural rules for the locale in play.
- Seeded translation defects live in
  `translations/seeded/fr.overrides.json`, applied on top of `fr.json`
  only when `SEEDED_DEFECTS=1` (supports both value overrides and key
  deletion, for the i18next-fallback-triggering defect).
  Structural/formatting/CSS defects are gated by a `seeded_fr` flag
  computed per-request and threaded into templates/routes explicitly.
- `webapp/formatting.py`: all Babel-backed currency/date/percent
  formatting funnels through here.
- Static assets (`static/`) live at the project root, not inside the
  `webapp/` package — `create_app()` must pass an explicit
  `static_folder` pointing there (Flask's default resolves relative to
  the package's `root_path`, i.e. `webapp/static`, which doesn't exist).
- `ground_truth/pages.py` is the single source of truth for page name →
  fr page path(s), used by both `tests/test_defects.py` and
  `scoring/ground_truth.py`. `"header"` maps to every page's path since
  the header renders on all of them; every other page maps to one path.
- `scoring/matcher.py` matches findings against `defects.yaml` only for
  the seeded build (in clean mode nothing is actually wrong, so a hit on
  a defect's element is a false positive, not a detection), then against
  `ground_truth/known_issues.yaml` (pre-existing, unseeded issues; a
  match there counts toward neither recall nor false positives — see its
  own report section), then against `controls.yaml` filtered to entries
  where `fr_seeded == fr_clean` (drops C10 and C11, the two controls that
  don't hold in seeded mode — A06/A07 cover those elements there
  instead). A defect match always wins over a known-issue match at the
  same testid, e.g. on the seeded French landing page a finding on
  `landing-banner-image` is always credited to A06, never U01. A couple
  of defects need testid-less fallback overrides instead of
  text-containment matching: D07 (`fr_seeded` is the bare string `"en"`)
  and A06 (its "text" is an image filename, not rendered text) — see
  `FALLBACK_OVERRIDES` in that module before changing either entry's
  `fr_seeded` value.
