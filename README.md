# Northstar Bank — bilingual (en / fr-CA) demo app

A small Flask demo bank app used as the target application for a proof of
concept on AI-assisted i18n testing. It serves English and French
(Quebec / fr-CA) pages and runs in two build modes, described below.

This repo does **not** document which strings or elements are correct or
incorrect in which mode — that catalog is intentionally kept out of this
README. See `ground_truth/` if you are the person maintaining this app;
it must not be shared with, or read by, any test suite exercising it.

## Stack

- Python 3.14, Flask, Jinja2 templates
- Babel for locale-aware currency, date, and percentage formatting, and
  CLDR plural rules
- A minimal custom i18next-style translation helper (`webapp/i18n.py`)
- Plain CSS, no frontend framework
- pytest for self-verification tests

## Environment

- The project lives on **Windows**. Docker Engine is **not** installed on
  Windows — it runs inside **WSL2 Ubuntu** and is invoked from Windows
  through `wsl.exe`.
- Python tooling on Windows is [`uv`](https://docs.astral.sh/uv/) with
  Python 3.14.
- WSL2 distro `Ubuntu` has Docker Engine + the Compose plugin installed
  (not Docker Desktop).

### Running Docker commands from Windows

Always call Docker as:

```
wsl -d Ubuntu -- docker ...
wsl -d Ubuntu -- docker compose ...
```

Run these from the project root in a Windows shell (PowerShell or Git
Bash). `wsl.exe` maps the current Windows directory to its
`/mnt/<drive>/...` equivalent, so Docker sees the project files there.

If Git Bash mangles path arguments passed to `wsl.exe`, prefix the
command with `MSYS_NO_PATHCONV=1`, or stick to relative paths.

Optional PowerShell helper, so you can just type `docker ...`:

```powershell
function docker { wsl -d Ubuntu -- docker @args }
```

## Running with Docker (recommended)

From the project root:

```
wsl -d Ubuntu -- docker compose up -d --build
```

This builds and starts two containers from the same image:

| Build  | Port | `SEEDED_DEFECTS` |
|--------|------|-------------------|
| clean  | 5001 | `0` |
| seeded | 5002 | `1` |

Open in a Windows browser:

- http://localhost:5001/
- http://localhost:5002/

Health checks:

```
curl http://localhost:5001/health
curl http://localhost:5002/health
```

Each returns `{"status": "ok", "build": "clean" | "seeded"}`.

Source is built into the image — the default `docker-compose.yml` does
**not** bind-mount source from Windows, since bind mounts from the
Windows filesystem are slow and file-watching across the WSL2/Windows
boundary is unreliable. Rebuild the image (`--build`) after changing
source to see the change in the containers.

### Troubleshooting

- **Containers not reachable / "connection refused":** if WSL2 was
  stopped or restarted, its containers are not running. Start WSL first
  (`wsl -d Ubuntu`) and re-run `docker compose up -d`.
- **Path issues from Git Bash:** prefix commands with
  `MSYS_NO_PATHCONV=1` or use relative paths only.

## Running locally on Windows without Docker

```powershell
uv sync
$env:SEEDED_DEFECTS = "0"
$env:APP_TODAY = "2026-09-16"
$env:FLASK_APP = "wsgi:app"
uv run flask run --host=0.0.0.0 --port=5000
```

For the seeded build in a separate shell/port:

```powershell
uv sync
$env:SEEDED_DEFECTS = "1"
$env:APP_TODAY = "2026-09-16"
$env:FLASK_APP = "wsgi:app"
uv run flask run --host=0.0.0.0 --port=5001
```

## Build modes

- `SEEDED_DEFECTS` (`0` clean / `1` seeded) — set as a container
  environment variable, or as a shell env var for a local run.
- `APP_TODAY` (default `2026-09-16`) fixes "today" so dates are
  reproducible. All demo data is a fixed fixture; there is no randomness
  anywhere in the app.
- Timezone is `America/Toronto`, set explicitly in the app/containers —
  it does not depend on the host's timezone.

## URL map

Locale is a URL path prefix (`en` or `fr`). `/` redirects based on the
`Accept-Language` header (`fr*` → `/fr/`, otherwise `/en/`).

| Path | Page |
|---|---|
| `/health` | JSON health check |
| `/<lang>/` | Landing page |
| `/<lang>/calculator` | Loan calculator |
| `/<lang>/apply` | Loan application form |
| `/<lang>/application/<id>` | Application summary |
| `/<lang>/dashboard` | Account dashboard |

## Tests

Self-verification tests live in `tests/` and run against either an
in-process Flask app or a running deployment (e.g. the Docker
containers).

In-process (default):

```powershell
uv sync
uv run pytest -q
```

Against the running containers:

```powershell
$env:POC_BASE_URL_CLEAN = "http://localhost:5001"
$env:POC_BASE_URL_SEEDED = "http://localhost:5002"
uv run pytest -q
```

(Bash/WSL equivalent: `POC_BASE_URL_CLEAN=http://localhost:5001 POC_BASE_URL_SEEDED=http://localhost:5002 uv run pytest -q`.)

## Scoring AI test findings

A separate repo holds the AI test suite for this app (deterministic
Playwright checks, an AI judge, an AI explorer agent), each emitting
findings in the shared format defined by `scoring/findings.schema.json` —
that schema file is the only thing shared with that repo. The scorer that
grades findings against this repo's ground truth stays here:

```powershell
uv run python -m scoring.score --findings <file-or-folder-of-findings.json> --build seeded --out out/
uv run python -m scoring.score --findings <file-or-folder-of-findings.json> --build clean --out out/
```

`--findings` accepts a single findings file or a folder of them (a folder
also reports run-to-run stability per defect). `--build` must match which
build the findings were collected against. Every input file is validated
against the schema first; if any file fails validation, the run aborts
with a per-file error list rather than scoring a partial set.

Output is `report.json` and `report.md` in `--out`, broken down per
findings source, with detected/missed counts, a per-defect table,
false positives on controls, unclassified findings for manual review,
precision/recall, and (with multiple runs) stability. These reports
contain defect IDs and ground-truth text — see `CLAUDE.md` for the rule
on keeping that out of the test repo.

### Comparing deterministic and AI judge findings

`scoring.compare` puts the deterministic checks and the AI judge side by
side for one test run and writes a single Markdown file:

```powershell
uv run python -m scoring.compare `
  --det-seeded <run>/seeded/findings.json `
  --det-clean <run>/clean/findings.json `
  --ai-seeded <run>/seeded/findings-ai-judge-1.json `
  --ai-clean <run>/clean/findings-ai-judge-1.json `
  --ai-stability <folder-of-seeded-ai-judge-repeats> `
  --out scoring/reports/comparison.md
```

`<run>` is a run folder under the test repo's `artifacts/`. The
`--ai-stability` folder must contain only the seeded AI judge repeat
files — copy them into a separate folder so the deterministic
`findings.json` and the single run are not picked up. Keep the original
file names, because they are looked up in `judge-manifest.json`.

The report covers per-defect detection for the deterministic checks, the
AI judge, and their union; recall per expected layer; false positives on
controls and on the clean build, with the text of each finding; run-to-run
stability across the repeats; and calls, tokens, notional cost, and
duration. Call counts and the full cost of runs that were resumed from
cache come from `judge-manifest.json` and the `calls.json` files it
references, which must sit next to the `--ai-seeded` and `--ai-clean`
files. Like the scorer's reports, the output contains defect IDs and
ground-truth text.

## Regenerating the banner images

The landing-page banners are pre-rendered PNGs, committed to the repo so
output is identical on every machine (the text is baked into the pixels
using a bundled font, not the host's fonts). Regenerate them with:

```
uv run python scripts/make_banners.py
```

The font (`fonts/NotoSans-Regular.ttf`, SIL Open Font License, see
`fonts/OFL.txt`) is bundled in the repo for this reason.
