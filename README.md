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

## Quick start: run the app locally

These steps run both builds of the app directly on Windows, with no
Docker. Every command below is for **PowerShell**.

The app always runs as two separate servers, one per build:

| Build  | Port | `SEEDED_DEFECTS` |
|--------|------|-------------------|
| clean  | 5001 | `0` |
| seeded | 5002 | `1` |

### Prerequisites

- Windows 10 or 11.
- [`uv`](https://docs.astral.sh/uv/), the Python package and project
  manager. Install it with:

  ```powershell
  winget install --id astral-sh.uv -e
  ```

  Then close and reopen PowerShell so `uv` is on your `PATH`. Check it
  with `uv --version`.
- You don't need to install Python yourself. The app needs Python 3.14,
  and `uv` downloads it automatically in step 1 if it isn't already
  installed.
- A copy of this repository. Clone it, or unpack the archive you were
  given.

### 1. Install the dependencies

Open PowerShell in the repository's root folder (the folder that
contains `pyproject.toml`) and run:

```powershell
uv sync
```

This creates a `.venv` folder with Python 3.14 and all dependencies. You
only need to do this once, and again after pulling changes that touch
`pyproject.toml` or `uv.lock`.

### 2. Start the clean build

The local servers and the Docker containers (see
[Running with Docker](#running-with-docker)) use the same ports, so run
one or the other, never both. If you have started the Docker containers,
stop them first (see [Stop](#stop)). The local server does not report a
busy port: it prints `Running on ...` as usual, and you can't tell
whether your requests reach it or the container.

In the same PowerShell window:

```powershell
$env:SEEDED_DEFECTS = "0"
uv run flask --app wsgi:app run --port 5001
```

You should see:

```
 * Serving Flask app 'wsgi:app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
```

The `WARNING` line is normal. Leave this window open: the server runs
until you stop it.

### 3. Start the seeded build

Open a **second** PowerShell window in the same root folder and run:

```powershell
$env:SEEDED_DEFECTS = "1"
uv run flask --app wsgi:app run --port 5002
```

The output is the same as in step 2, except that it ends with
`Running on http://127.0.0.1:5002`.

Always set `SEEDED_DEFECTS` explicitly before starting a server. The
value stays set in that PowerShell window until you close it, so a
leftover `"1"` would start the seeded build on the clean port.

### 4. Check that it works

Open these pages in a browser:

| | Clean build | Seeded build |
|---|---|---|
| English | http://127.0.0.1:5001/en/ | http://127.0.0.1:5002/en/ |
| French  | http://127.0.0.1:5001/fr/ | http://127.0.0.1:5002/fr/ |

The root URL (`/`) redirects to `/en/` or `/fr/` according to your
browser's language, so use the links above to open a specific language.

To check from the command line, open a third PowerShell window and run:

```powershell
curl.exe http://127.0.0.1:5001/health
curl.exe http://127.0.0.1:5002/health
```

They should print `{"build":"clean","status":"ok"}` and
`{"build":"seeded","status":"ok"}`. Type `curl.exe`, not `curl`: in
Windows PowerShell 5.1, `curl` is an alias for `Invoke-WebRequest`.

Use `127.0.0.1` rather than `localhost` for the local servers. They
listen on IPv4 only, and some clients try IPv6 (`::1`) first for
`localhost`, which adds about 2 seconds to every request. Python's
`requests` library, which the test suite uses, is one of them.

### 5. Stop the servers

Press `Ctrl+C` in each server window. Stop them before you start the
Docker containers on the same ports.

## Running with Docker

This is an alternative to the local run above. It runs the same two
builds, on the same ports, in Docker containers.

On the maintainer's machine, Docker Engine and the Compose plugin are
installed inside **WSL2 Ubuntu** (distro `Ubuntu`), not as Docker
Desktop, so every Docker command is called from Windows through
`wsl.exe`:

```
wsl -d Ubuntu -- docker ...
wsl -d Ubuntu -- docker compose ...
```

Run these from the repository's root folder in PowerShell or Git Bash.
`wsl.exe` maps the current Windows directory to its `/mnt/<drive>/...`
equivalent, so Docker sees the project files there. If Git Bash mangles
path arguments passed to `wsl.exe`, prefix the command with
`MSYS_NO_PATHCONV=1`, or use relative paths only.

If you use Docker Desktop instead, run the same commands without the
`wsl -d Ubuntu --` prefix. This setup hasn't been tested with this
project.

Optional PowerShell helper, so you can just type `docker ...`:

```powershell
function docker { wsl -d Ubuntu -- docker @args }
```

### Start

1. Open a separate PowerShell window, run the following, and leave the
   window open for as long as you need the containers:

   ```
   wsl -d Ubuntu
   ```

   WSL shuts the `Ubuntu` distro down shortly after the last WSL window
   or command exits, and the containers stop with it. On the maintainer's
   machine (WSL 2.7.14) they stopped 15–30 seconds after
   `docker compose up -d` returned when nothing else kept WSL open.

2. In another PowerShell window, from the repository's root folder:

   ```
   wsl -d Ubuntu -- docker compose up -d --build
   ```

This builds one image and starts two containers from it, `clean` on
port 5001 and `seeded` on port 5002. Check them with:

```powershell
curl.exe http://localhost:5001/health
curl.exe http://localhost:5002/health
```

They should print `{"build":"clean","status":"ok"}` and
`{"build":"seeded","status":"ok"}`. The pages are at the same paths as in
the local run, for example http://localhost:5001/fr/. The containers
listen on both IPv4 and IPv6, so `localhost` is fine here.

### Stop

```
wsl -d Ubuntu -- docker compose stop
```

Source is built into the image — the default `docker-compose.yml` does
**not** bind-mount source from Windows, since bind mounts from the
Windows filesystem are slow and file-watching across the WSL2/Windows
boundary is unreliable. Rebuild the image (`--build`) after changing
source to see the change in the containers.

### Troubleshooting

- **Containers not reachable / "connection refused":** the `Ubuntu`
  distro was shut down, which stops its containers (they show as
  `Exited (255)` in `wsl -d Ubuntu -- docker ps -a`). This happens when
  no WSL window was left open (see step 1 of [Start](#start)), or after
  WSL was stopped or restarted. Open a WSL window and re-run
  `wsl -d Ubuntu -- docker compose up -d`.
- **Unexpected responses on port 5001 or 5002:** check that no local
  server from the quick start is still running on the same port, and
  stop it with `Ctrl+C`.
- **Path issues from Git Bash:** prefix commands with
  `MSYS_NO_PATHCONV=1` or use relative paths only.

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

Against running servers (the local servers from the quick start, or the
Docker containers):

```powershell
$env:POC_BASE_URL_CLEAN = "http://127.0.0.1:5001"
$env:POC_BASE_URL_SEEDED = "http://127.0.0.1:5002"
uv run pytest -q
```

(Bash/WSL equivalent: `POC_BASE_URL_CLEAN=http://127.0.0.1:5001 POC_BASE_URL_SEEDED=http://127.0.0.1:5002 uv run pytest -q`.)

Use `127.0.0.1`, not `localhost`: against the local servers, `localhost`
makes every request about 2 seconds slower (see step 4 of the quick
start), and the full run takes minutes instead of seconds.

These variables stay set in that PowerShell window. To go back to the
in-process run there, clear them first:
`Remove-Item Env:POC_BASE_URL_CLEAN, Env:POC_BASE_URL_SEEDED`.

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
