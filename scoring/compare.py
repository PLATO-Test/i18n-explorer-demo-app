"""Comparison CLI: deterministic (phase 1) vs AI judge (phase 2), and
optionally AI explorer (phase 3), findings for one test run, written as a
single Markdown report.

    uv run python -m scoring.compare \\
        --det-seeded <run>/seeded/findings.json --det-clean <run>/clean/findings.json \\
        --ai-seeded <run>/seeded/findings-ai-judge-1.json --ai-clean <run>/clean/findings-ai-judge-1.json \\
        --ai-stability <folder of seeded AI judge repeats> \\
        [--explorer-seeded <run>/seeded/findings-ai-explorer-1.json \\
         --explorer-clean <run>/clean/findings-ai-explorer-1.json \\
         --explorer-stability <folder of complete seeded AI explorer runs>] \\
        --out <comparison.md>

The three --explorer-* options go together; without them the output is the
two-approach comparison.

Call counts come from judge-manifest.json next to --ai-seeded / --ai-clean,
and snapshot capture time from run.json next to --det-seeded / --det-clean.
Stability files are looked up by file name in the seeded manifest, so a
folder of copies works as long as the names are unchanged. Explorer tool
calls, screenshots and coverage come from explorer/<n>/manifest.json and
coverage.json next to the explorer findings files, where <n> is the file
name's numeric suffix.

Like scoring.score, the output contains defect IDs and ground-truth text.
Never copy it into, or generate it for, the separate AI test suite repo -
see CLAUDE.md.
"""
import argparse
import json
import os
import sys
from pathlib import Path
from statistics import mean

from scoring.findings import FindingsValidationError, Run, load_runs
from scoring.ground_truth import Entry, KnownIssue, load_controls, load_defects, load_known_issues
from scoring.report import LAYERS, build_report

NUMBER_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def _yn(b: bool) -> str:
    return "yes" if b else "no"


def _cell(s) -> str:
    if s is None:
        return "-"
    return str(s).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _suffix(path: Path) -> str:
    """'findings-ai-judge-3.json' -> '3'."""
    return path.stem.rsplit("-", 1)[1]


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _score(
    path: Path, build: str, defects: list[Entry], controls: list[Entry], known_issues: list[KnownIssue]
) -> tuple[dict, list[Run]]:
    runs = load_runs(path)
    if not runs:
        raise SystemExit(f"No findings files found at {path}")
    report = build_report(runs, defects, controls, build, known_issues)
    if len(report["sources"]) != 1:
        raise SystemExit(f"{path}: expected one findings source, got {sorted(report['sources'])}")
    return next(iter(report["sources"].values())), runs


def _detected(sr: dict) -> dict[str, bool]:
    return {row["id"]: row["detected"] for row in sr["defect_table"]}


def _explorer_meta(build_dir: Path, findings_file: Path) -> dict:
    """manifest.json and coverage.json of the explorer run behind a findings
    file: <build dir>/explorer/<n>/, n being the file name's suffix."""
    run_dir = build_dir / "explorer" / _suffix(findings_file)
    return {
        "manifest": _read_json(run_dir / "manifest.json"),
        "coverage": _read_json(run_dir / "coverage.json"),
    }


def _explorer_usage(manifest: dict) -> dict[str, int]:
    """Token totals summed over every model in manifest["model_usage"], the
    same source the findings file's run block and the cost come from."""
    mu = manifest["model_usage"].values()
    return {
        "fresh": sum(u["inputTokens"] for u in mu),
        "cache_read": sum(u["cacheReadInputTokens"] for u in mu),
        "cache_write": sum(u["cacheCreationInputTokens"] for u in mu),
        "output": sum(u["outputTokens"] for u in mu),
    }


def _explorer_pages(coverage: dict, locale: str) -> str:
    s = coverage["summary"][locale]
    return f"{s['pages_reached']}/{s['pages']}"


def _explorer_states(coverage: dict, locale: str) -> str:
    s = coverage["summary"][locale]
    return f"{s['states_reached']}/{s['states_configured']}"


class Manifest:
    """judge-manifest.json for one build, plus the calls.json files it points at."""

    def __init__(self, build_dir: Path):
        self.build_dir = build_dir
        self.entries = _read_json(build_dir / "judge-manifest.json")["entries"]

    def entry_for(self, file_name: str) -> dict:
        for e in self.entries:
            if e.get("file") == file_name:
                return e
        raise SystemExit(f"{file_name} not found in {self.build_dir / 'judge-manifest.json'}")

    def live_calls(self, entry: dict) -> list[dict]:
        calls = _read_json(self.build_dir / entry["calls_file"])["calls"]
        return [c for c in calls if not c.get("cached")]

    def whole_pass(self, file_name: str) -> dict:
        """Live calls of every single-run invocation that led to file_name:
        the one that wrote it plus the failed attempts right before it,
        whose responses it reused from cache."""
        def zero() -> dict:
            return {"in": 0, "out": 0, "cost": 0.0, "dur": 0.0, "live": 0, "invocations": 0}

        tot = zero()
        for e in self.entries:
            if e["pass"] != 1 or e.get("kind") == "repeat":
                continue
            calls = self.live_calls(e)
            tot["in"] += sum(c.get("input_tokens") or 0 for c in calls)
            tot["out"] += sum(c.get("output_tokens") or 0 for c in calls)
            tot["cost"] += sum(c.get("cost_usd") or 0 for c in calls)
            tot["dur"] += sum(c.get("duration_s") or 0 for c in calls)
            tot["live"] += len(calls)
            tot["invocations"] += 1
            if e.get("file") == file_name:
                return tot
            if e["status"] == "ok":
                # an earlier successful single run - not part of this one
                tot = zero()
        raise SystemExit(f"{file_name} not found in {self.build_dir / 'judge-manifest.json'}")

    def cost_bases(self) -> set[str | None]:
        bases = set()
        for e in self.entries:
            for c in self.live_calls(e):
                for usage in ((c.get("usage_breakdown") or {}).get("modelUsage") or {}).values():
                    bases.add(usage.get("costBasis"))
        return bases


def _explorer_cost_section(
    args, s1: Run, c1: Run, meta_s1: dict, meta_c1: dict, stab_runs: list[Run], meta_stab: list[dict],
    n_word: str, det_run: Run, judge_runs: list[Run], judge_entries: list[dict], judge_live: bool,
) -> list[str]:
    """Section 5, explorer part: cost, tool calls, screenshots and coverage,
    plus a one-pass summary of all three approaches."""
    def run_line(label: str, run: Run, meta: dict) -> str:
        m = meta["manifest"]
        b = m["budget_used"]
        u = _explorer_usage(m)
        cost = f"${run.cost_usd:.4f}" if run.cost_usd is not None else "-"
        return (
            f"| {label} | {m['status']} | {b['turns']} | {b['tool_calls']} | {b['screenshots']} | "
            f"{run.input_tokens:,} | {u['cache_read']:,} | {u['cache_write']:,} | "
            f"{u['fresh']:,} | {run.output_tokens:,} | {cost} | {run.duration_s:.1f} |"
        )

    rows = [
        (f"seeded run {_suffix(s1.file_path)} (single run)", s1, meta_s1),
        (f"clean run {_suffix(c1.file_path)} (single run)", c1, meta_c1),
    ]
    rows += [
        (f"seeded run {_suffix(r.file_path)} (stability)", r, meta)
        for r, meta in zip(stab_runs, meta_stab)
        if r.file_path.name != s1.file_path.name
    ]
    L = [
        "### AI explorer: calls, tokens, notional cost, duration",
        "",
        "Tokens, cost and duration come from each findings file's `run` block, and status, model turns, tool calls and",
        "screenshots from `explorer/<n>/manifest.json`. \"input total\" is the `run` block's `input_tokens`: fresh input,",
        "cache reads and cache writes of all models used (the pinned model and a small Haiku helper), summed. The three",
        "parts come from the manifest's `model_usage`, which is also the source of the `run` block and the cost.",
        "Model turns are assistant turns (one model call each). Tool calls are the browser tool calls the agent made.",
        "",
        "| run | status | model turns | tool calls | screenshots | input total | cache read | cache write | "
        "fresh input | output tokens | notional cost (USD) | duration (s) |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    L += [run_line(label, run, meta) for label, run, meta in rows]
    in_stab = {_suffix(r.file_path) for r in stab_runs}
    explorer_dir = args.explorer_seeded.parent / "explorer"
    for d in sorted(explorer_dir.iterdir(), key=lambda p: p.name):
        if d.is_dir() and d.name not in in_stab:
            m = _read_json(d / "manifest.json")
            b = m["budget_used"]
            u = _explorer_usage(m)
            tin = u["fresh"] + u["cache_read"] + u["cache_write"]
            L.append(
                f"| seeded run {d.name} (excluded from stability) | {m['status']} | {b['turns']} | "
                f"{b['tool_calls']} | {b['screenshots']} | {tin:,} | {u['cache_read']:,} | {u['cache_write']:,} | "
                f"{u['fresh']:,} | {u['output']:,} | ${m['cost_usd']:.4f} | {m['duration_s']:.1f} |"
            )
    basis = {meta["manifest"]["cost_basis"] for _, _, meta in rows}
    L += ["", f"Cost basis reported by the harness: {', '.join(f'`{b}`' for b in sorted(basis))}."]
    finished = [m for m in (meta["manifest"] for _, _, meta in rows) if m["interrupted"] and m["finish_called"]]
    if finished:
        L += [
            "",
            f"Note: {len(finished)} of {len(rows)} runs above report `interrupted: true` together with "
            "`finish_called: true`"
            + (
                " (and `result_subtype: error_during_execution`)"
                if all(m.get("result_subtype") == "error_during_execution" for m in finished)
                else ""
            )
            + ". This is expected harness behaviour: the wind-down stops the session after the agent calls "
            "`finish`. It is not a failed run.",
        ]
    mismatched = []
    for label, _, meta in rows:
        m = meta["manifest"]
        u = _explorer_usage(m)
        t = m["tokens"]
        main = m["model_usage"].get(m["model_pinned"])
        if main is not None and main["cacheReadInputTokens"] != t["cache_read_input_tokens"]:
            mismatched.append((label, main["cacheReadInputTokens"] + main["cacheCreationInputTokens"] + main["inputTokens"],
                               t["cache_read_input_tokens"] + t["cache_creation_input_tokens"] + t["input_tokens"]))
    for label, from_usage, from_turns in mismatched:
        L += [
            "",
            f"Note: for {label}, the manifest's per-turn token totals ({from_turns:,} input tokens) exceed its "
            f"`model_usage` for the pinned model ({from_usage:,}). The table uses `model_usage`, the source of the "
            "`run` block and of the reported cost, so nothing here confirms it. If the per-turn totals are the right "
            f"ones, this run's input tokens are {from_turns - from_usage:,} higher and its cost is understated too.",
        ]
    L += [
        "",
        "### AI explorer: pages covered per locale",
        "",
        "From `explorer/<n>/coverage.json`: pages reached / pages in the page map, and configured states reached /",
        "configured states. `coverage.json` describes its own method as a post-run proxy from the trajectory.",
        "",
        "| run | en pages | fr pages | en states | fr states |",
        "|---|---|---|---|---|",
    ]
    for label, _, meta in rows:
        cov = meta["coverage"]
        L.append(
            f"| {label} | {_explorer_pages(cov, 'en')} | {_explorer_pages(cov, 'fr')} | "
            f"{_explorer_states(cov, 'en')} | {_explorer_states(cov, 'fr')} |"
        )
    understated = [
        label for label, _, meta in rows
        if any(
            v["path"] is None
            and any(p.startswith(f"/{v['locale']}/application/") for p in meta["coverage"]["visited_paths_not_in_config"])
            for v in meta["coverage"]["never_visited"]
        )
    ]
    if understated:
        L += [
            "",
            f"Note: in {len(understated)} of {len(rows)} runs above, `coverage.json` lists a page as never visited "
            "although `visited_paths_not_in_config` holds a path of that page (the English application summary, whose "
            "page map has no path). The proxy does not credit that visit, so the page count for that locale is one too low.",
        ]
    L += [
        "",
        "### One pass per approach",
        "",
        f"Mean over the runs used for stability, seeded build: deterministic is a single run, the AI judge is its "
        f"{len(judge_runs)} repeats, the AI explorer is its {n_word} complete runs.",
        "",
        "| approach | model calls | tool calls | input tokens | output tokens | notional cost (USD) | duration (s) |",
        "|---|---|---|---|---|---|---|",
        f"| deterministic | 0 | - | 0 | 0 | $0 | {det_run.duration_s:.3f} |",
        f"| AI judge | {mean(e['model_calls'] for e in judge_entries):.0f} | - | "
        f"{mean(r.input_tokens for r in judge_runs):,.0f} | {mean(r.output_tokens for r in judge_runs):,.0f} | "
        f"${mean(r.cost_usd for r in judge_runs):.3f} | {mean(r.duration_s for r in judge_runs):.0f} |",
        f"| AI explorer | {mean(m['manifest']['budget_used']['turns'] for m in meta_stab):.0f} | "
        f"{mean(m['manifest']['budget_used']['tool_calls'] for m in meta_stab):.0f} | "
        f"{mean(r.input_tokens for r in stab_runs):,.0f} | {mean(r.output_tokens for r in stab_runs):,.0f} | "
        f"${mean(r.cost_usd for r in stab_runs):.3f} | {mean(r.duration_s for r in stab_runs):.0f} |",
        "",
        "AI judge model calls are live calls per pass" + ("" if judge_live else " (some repeats also used cached calls)")
        + ". AI explorer model calls are assistant turns.",
        "",
    ]
    return L


def build_comparison(args: argparse.Namespace) -> str:
    defects = load_defects()
    controls = load_controls()
    known_issues = load_known_issues()

    det_seeded, det_seeded_runs = _score(args.det_seeded, "seeded", defects, controls, known_issues)
    det_clean, det_clean_runs = _score(args.det_clean, "clean", defects, controls, known_issues)
    ai_seeded, ai_seeded_runs = _score(args.ai_seeded, "seeded", defects, controls, known_issues)
    ai_clean, ai_clean_runs = _score(args.ai_clean, "clean", defects, controls, known_issues)
    ai_stab, ai_stab_runs = _score(args.ai_stability, "seeded", defects, controls, known_issues)
    if len(ai_stab_runs) < 2:
        raise SystemExit(f"--ai-stability needs at least 2 runs, found {len(ai_stab_runs)} in {args.ai_stability}")
    n_rep = len(ai_stab_runs)
    n_rep_word = NUMBER_WORDS.get(n_rep, str(n_rep))

    explorer_args = (args.explorer_seeded, args.explorer_clean, args.explorer_stability)
    ex = any(a is not None for a in explorer_args)
    if ex and any(a is None for a in explorer_args):
        raise SystemExit("--explorer-seeded, --explorer-clean and --explorer-stability must be given together")
    if ex:
        ex_seeded, ex_seeded_runs = _score(args.explorer_seeded, "seeded", defects, controls, known_issues)
        ex_clean, ex_clean_runs = _score(args.explorer_clean, "clean", defects, controls, known_issues)
        ex_stab, ex_stab_runs = _score(args.explorer_stability, "seeded", defects, controls, known_issues)
        if len(ex_stab_runs) < 2:
            raise SystemExit(
                f"--explorer-stability needs at least 2 runs, found {len(ex_stab_runs)} in {args.explorer_stability}"
            )
        n_ex = len(ex_stab_runs)
        n_ex_word = NUMBER_WORDS.get(n_ex, str(n_ex))
        # Stability files may be copies, so manifests are always read from the seeded build dir.
        ex_meta_s1 = _explorer_meta(args.explorer_seeded.parent, args.explorer_seeded)
        ex_meta_c1 = _explorer_meta(args.explorer_clean.parent, args.explorer_clean)
        ex_meta_stab = [_explorer_meta(args.explorer_seeded.parent, r.file_path) for r in ex_stab_runs]
        for r, meta in zip(ex_stab_runs, ex_meta_stab):
            if meta["manifest"]["status"] != "completed":
                raise SystemExit(
                    f"{r.file_path.name}: explorer status is {meta['manifest']['status']!r}, not 'completed'; "
                    "score partial runs separately and keep them out of --explorer-stability"
                )

    seeded_manifest = Manifest(args.ai_seeded.parent)
    clean_manifest = Manifest(args.ai_clean.parent)

    det = _detected(det_seeded)
    ai = _detected(ai_seeded)
    union = {d.id: det[d.id] or ai[d.id] for d in defects}
    n = len(defects)
    if ex:
        exp = _detected(ex_seeded)
        union = {d.id: det[d.id] or ai[d.id] or exp[d.id] for d in defects}

    inputs = [args.det_seeded, args.det_clean, args.ai_seeded, args.ai_clean]
    if ex:
        inputs += [args.explorer_seeded, args.explorer_clean]
    base = Path(os.path.commonpath([os.path.abspath(p) for p in inputs]))

    def rel(p: Path) -> str:
        return Path(os.path.abspath(p)).relative_to(base).as_posix()

    base_shown = Path(os.path.relpath(base)).as_posix()
    seeded_dir = rel(args.ai_seeded.parent)
    stab_files = [r.file_path for r in ai_stab_runs]
    stab_shown = ", ".join(
        [f"`{seeded_dir}/{stab_files[0].name}`"] + [f"`-{_suffix(p)}{p.suffix}`" for p in stab_files[1:]]
    )

    L: list[str] = []
    title = "Phase 1 vs phase 2 vs phase 3 comparison" if ex else "Phase 1 vs phase 2 comparison"
    L += [
        f"# {title} - run {ai_seeded_runs[0].run_id}",
        "",
        f"Inputs (all under `{base_shown}/`):",
        "",
        f"- Phase 1 deterministic: `{rel(args.det_seeded)}`, `{rel(args.det_clean)}`",
        f"- Phase 2 AI judge, single run: `{rel(args.ai_seeded)}`, `{rel(args.ai_clean)}`",
        f"- Phase 2 AI judge, stability: {stab_shown} (seeded only, no clean repeats)",
    ]
    if ex:
        ex_seeded_dir = rel(args.explorer_seeded.parent)
        ex_stab_shown = ", ".join(
            [f"`{ex_seeded_dir}/{ex_stab_runs[0].file_path.name}`"]
            + [f"`-{_suffix(r.file_path)}{r.file_path.suffix}`" for r in ex_stab_runs[1:]]
        )
        L += [
            f"- Phase 3 AI explorer, single run: `{rel(args.explorer_seeded)}`, `{rel(args.explorer_clean)}`",
            f"- Phase 3 AI explorer, stability: {ex_stab_shown} (seeded only, complete runs only, no clean repeats)",
            f"- Phase 3 AI explorer, per-run manifests and coverage: `{ex_seeded_dir}/explorer/<n>/manifest.json`, `coverage.json`",
        ]
    L += [
        "",
        "All inputs were scored in memory with `scoring.report.build_report`, the same code behind `scoring.score`.",
        f"The \"AI judge\" columns in sections 1-3 are single run {_suffix(args.ai_seeded)}"
        + (f" and the \"AI explorer\" columns single run {_suffix(args.explorer_seeded)}. " if ex else ". ")
        + "Repeats appear only in section 4.",
        "",
    ]

    # 1. Per-defect
    if ex:
        L += [
            "## 1. Per-defect detection (seeded build)",
            "",
            "| id | category | expected_layer | deterministic | AI judge | AI explorer | union of all three |",
            "|---|---|---|---|---|---|---|",
        ]
        for d in defects:
            L.append(
                f"| {d.id} | {d.category} | {d.expected_layer} | {_yn(det[d.id])} | {_yn(ai[d.id])} | "
                f"{_yn(exp[d.id])} | {_yn(union[d.id])} |"
            )
        L += [
            f"| **total** | | | **{sum(det.values())}/{n}** | **{sum(ai.values())}/{n}** | "
            f"**{sum(exp.values())}/{n}** | **{sum(union.values())}/{n}** |",
            "",
        ]
        by_approach = (("deterministic", det), ("AI judge", ai), ("AI explorer", exp))
        L += ["Defects found by exactly one approach:", "", "| approach | only this approach found |", "|---|---|"]
        for name, hits in by_approach:
            only = [
                d.id for d in defects
                if hits[d.id] and not any(other[d.id] for other_name, other in by_approach if other_name != name)
            ]
            L.append(f"| {name} | {', '.join(only) or 'none'} |")
        missed = [d.id for d in defects if not union[d.id]]
        L += [f"| none of the three | {', '.join(missed) or 'none'} |", ""]
    else:
        L += [
            "## 1. Per-defect detection (seeded build)",
            "",
            "| id | category | expected_layer | deterministic | AI judge | union |",
            "|---|---|---|---|---|---|",
        ]
        for d in defects:
            L.append(
                f"| {d.id} | {d.category} | {d.expected_layer} | {_yn(det[d.id])} | {_yn(ai[d.id])} | {_yn(union[d.id])} |"
            )
        L += [
            f"| **total** | | | **{sum(det.values())}/{n}** | **{sum(ai.values())}/{n}** | **{sum(union.values())}/{n}** |",
            "",
        ]

    # 2. Recall per layer
    L += [
        "## 2. Recall per expected_layer (seeded build)",
        "",
        "| approach | " + " | ".join(LAYERS) + " | overall |",
        "|---|" + "---|" * (len(LAYERS) + 1),
    ]
    recall_rows = [("deterministic", det), ("AI judge", ai)]
    if ex:
        recall_rows.append(("AI explorer", exp))
    recall_rows.append(("union of all three" if ex else "union", union))
    for name, hits in recall_rows:
        cells = []
        for layer in LAYERS:
            ids = [d.id for d in defects if d.expected_layer == layer]
            k = sum(hits[i] for i in ids)
            cells.append(f"{k}/{len(ids)} ({k / len(ids):.0%})")
        k = sum(hits.values())
        cells.append(f"{k}/{n} ({k / n:.0%})")
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    L.append("")

    # 3. False positives
    def fp_rows(sr: dict, runs: list[Run]) -> list[tuple[str, dict]]:
        """(scorer class, raw finding) for every control FP and unclassified finding."""
        raws = [f for r in runs for f in _read_json(r.file_path)["findings"]]

        def find_raw(ref: dict) -> dict:
            for f in raws:
                if f["observed"] == ref["observed"] and (f["data_testid"] or None) == ref["data_testid"]:
                    return f
            raise LookupError(ref)

        rows = []
        for fp in sr["control_false_positives"]:
            for ref in fp["findings"]:
                rows.append((f"control FP ({fp['control_id']})", find_raw(ref)))
        for ki in sr["known_issues"]:
            for ref in ki["findings"]:
                rows.append((f"known issue ({ki['issue_id']})", find_raw(ref)))
        for ref in sr["unclassified"]:
            rows.append(("unclassified", find_raw(ref)))
        return rows

    def fp_table(rows: list[tuple[str, dict]]) -> list[str]:
        if not rows:
            return ["None.", ""]
        out = [
            "| scorer class | page | testid | category | observed | expected | description |",
            "|---|---|---|---|---|---|---|",
        ]
        for cls, f in rows:
            out.append(
                f"| {cls} | {_cell(f['page_path'])} | {_cell(f['data_testid'])} | {_cell(f['category'])} | "
                f"{_cell(f['observed'])} | {_cell(f['expected'])} | {_cell(f['description'])} |"
            )
        return out + [""]

    approaches = [
        ("deterministic", "Deterministic", det_seeded, det_seeded_runs, det_clean, det_clean_runs),
        (f"AI judge (run {_suffix(args.ai_seeded)})", f"AI judge (run {_suffix(args.ai_seeded)})",
         ai_seeded, ai_seeded_runs, ai_clean, ai_clean_runs),
    ]
    if ex:
        approaches.append(
            (f"AI explorer (run {_suffix(args.explorer_seeded)})", f"AI explorer (run {_suffix(args.explorer_seeded)})",
             ex_seeded, ex_seeded_runs, ex_clean, ex_clean_runs)
        )
    L += [
        "## 3. False positives",
        "",
        "On the seeded build a finding is a false positive only if it lands on a control (a correct element).",
        "Findings that match neither a defect nor a control are \"unclassified\" and need manual review.",
        "On the clean build nothing is wrong, so every finding is a false positive - except a finding that lands",
        "on a known, pre-existing issue (ground_truth/known_issues.yaml), which counts toward neither.",
        "",
    ]
    if ex:
        L += [
            "| approach | seeded: control FPs | seeded: known issues | seeded: unclassified | seeded: total findings | "
            "clean: total findings | clean: known issues | clean: false positives |",
            "|---|---|---|---|---|---|---|---|",
        ]
    else:
        L += [
            "| approach | seeded: control FPs | seeded: unclassified | seeded: total findings | "
            "clean: total findings | clean: known issues | clean: false positives |",
            "|---|---|---|---|---|---|---|",
        ]
    for name, _, s_sr, s_runs, c_sr, c_runs in approaches:
        ctrl = sum(fp["count"] for fp in s_sr["control_false_positives"])
        seeded_known = sum(ki["count"] for ki in s_sr["known_issues"])
        clean_total = sum(len(r.findings) for r in c_runs)
        clean_known = sum(ki["count"] for ki in c_sr["known_issues"])
        seeded_known_cell = f" {seeded_known} |" if ex else ""
        L.append(
            f"| {name} | {ctrl} |{seeded_known_cell} {len(s_sr['unclassified'])} | "
            f"{sum(len(r.findings) for r in s_runs)} | "
            f"{clean_total} | {clean_known} | {clean_total - clean_known} |"
        )
    L.append("")
    if ex:
        issue_ids = [k.id for k in known_issues]
        L += [
            "Known-issue hits by id (single runs):",
            "",
            "| approach | build | " + " | ".join(issue_ids) + " |",
            "|---|---|" + "---|" * len(issue_ids),
        ]
        for name, _, s_sr, _, c_sr, _ in approaches:
            for build_name, sr in (("seeded", s_sr), ("clean", c_sr)):
                counts = {ki["issue_id"]: ki["count"] for ki in sr["known_issues"]}
                L.append(f"| {name} | {build_name} | " + " | ".join(str(counts.get(i, 0)) for i in issue_ids) + " |")
        L.append("")
    for _, heading, s_sr, s_runs, c_sr, c_runs in approaches:
        L += [f"### {heading} - seeded build", ""] + fp_table(fp_rows(s_sr, s_runs))
        L += [f"### {heading} - clean build", ""] + fp_table(fp_rows(c_sr, c_runs))

    stab_ctrl = sum(fp["count"] for fp in ai_stab["control_false_positives"])
    L += [
        f"The {n_rep_word} seeded stability repeats add {stab_ctrl} control FPs and "
        f"{len(ai_stab['unclassified'])} unclassified findings.",
        "No clean-build repeats were run, so the clean FP rate of the AI judge rests on one run.",
        "",
    ]
    if ex:
        ex_stab_ctrl = sum(fp["count"] for fp in ex_stab["control_false_positives"])
        ex_stab_known = sum(ki["count"] for ki in ex_stab["known_issues"])
        L += [
            f"Across all {n_ex_word} seeded AI explorer runs (single run {_suffix(args.explorer_seeded)} included): "
            f"{ex_stab_ctrl} control FPs, {len(ex_stab['unclassified'])} unclassified findings and "
            f"{ex_stab_known} known-issue hits. The clean FP rate of the AI explorer rests on one run.",
            "",
        ]

    # 4. Stability
    stab_entries = [seeded_manifest.entry_for(p.name) for p in stab_files]
    all_live = all(e.get("cache") == "bypassed" and e["model_calls"] == e["calls"] for e in stab_entries)
    stab_names = stab_files[0].stem.rsplit("-", 1)[0] + "-" + "/".join(_suffix(p) for p in stab_files) + ".json"
    if ex:
        ex_stab_names = (
            ex_stab_runs[0].file_path.stem.rsplit("-", 1)[0] + "-"
            + "/".join(_suffix(r.file_path) for r in ex_stab_runs) + ".json"
        )
        L += [
            f"## 4. Stability: AI judge ({n_rep} repeats) and AI explorer ({n_ex} complete runs), seeded build",
            "",
            f"AI judge source: `{stab_names}` "
            f"({'cache bypassed, every call live' if all_live else 'some calls served from cache'}).",
            f"AI explorer source: `{ex_stab_names}`, all with manifest status `completed`. "
            "Explorer runs that did not complete (a rate-limited run) are scored separately and excluded here.",
            "Deterministic is a single run of a deterministic check, so no repeat stability is reported for it.",
            "",
            f"| id | expected_layer | AI judge detected in (repeats) | AI judge run {_suffix(args.ai_seeded)} | "
            f"AI explorer detected in (runs {'/'.join(_suffix(r.file_path) for r in ex_stab_runs)}) |",
            "|---|---|---|---|---|",
        ]
        for d in defects:
            s = ai_stab["stability"][d.id]
            e = ex_stab["stability"][d.id]
            L.append(
                f"| {d.id} | {d.expected_layer} | {s['detected_runs']}/{s['total_runs']} | {_yn(ai[d.id])} | "
                f"{e['detected_runs']}/{e['total_runs']} |"
            )
    else:
        L += [
            f"## 4. Stability across the {n_rep} AI judge repeats (seeded build)",
            "",
            f"Source: `{stab_names}` ({'cache bypassed, every call live' if all_live else 'some calls served from cache'}).",
            "Deterministic is a single run of a deterministic check, so no repeat stability is reported for it.",
            "",
            f"| id | expected_layer | detected in | AI judge run {_suffix(args.ai_seeded)} |",
            "|---|---|---|---|",
        ]
        for d in defects:
            s = ai_stab["stability"][d.id]
            L.append(f"| {d.id} | {d.expected_layer} | {s['detected_runs']}/{s['total_runs']} | {_yn(ai[d.id])} |")
    per_run = [
        sum(
            row["detected"]
            for row in build_report([r], defects, controls, "seeded", known_issues)["sources"]["ai_judge"]["defect_table"]
        )
        for r in ai_stab_runs
    ]
    L += [
        "",
        f"AI judge defects detected per repeat: {', '.join(f'{k}/{n}' for k in per_run)}; "
        f"mean recall {ai_stab['recall']:.3f}.",
        "",
    ] if ex else [
        "",
        f"Defects detected per repeat: {', '.join(f'{k}/{n}' for k in per_run)}; "
        f"mean recall {ai_stab['recall']:.3f}.",
        "",
    ]
    if ex:
        ex_per_run = [
            sum(
                row["detected"]
                for row in build_report([r], defects, controls, "seeded", known_issues)["sources"]["ai_explorer"]["defect_table"]
            )
            for r in ex_stab_runs
        ]
        always = [d.id for d in defects if ex_stab["stability"][d.id]["detected_runs"] == n_ex]
        never = [d.id for d in defects if ex_stab["stability"][d.id]["detected_runs"] == 0]
        flaky = [d.id for d in defects if d.id not in always and d.id not in never]
        L += [
            f"AI explorer defects detected per run: {', '.join(f'{k}/{n}' for k in ex_per_run)}; "
            f"mean recall {ex_stab['recall']:.3f}.",
            f"Found in every run: {len(always)}. Found in some but not all runs: {', '.join(flaky) or 'none'}. "
            f"Never found: {', '.join(never) or 'none'}.",
            "",
        ]

    # 5. Cost
    def run_row(label: str, manifest: Manifest | None, run: Run) -> str:
        e = manifest.entry_for(run.file_path.name) if manifest is not None else None
        calls = f"{e['calls']} jobs / {e['model_calls']} live / {e['cache_hits']} cached" if e else "0 (no model)"
        cost = f"${run.cost_usd:.4f}" if run.cost_usd is not None else "$0"
        tin = f"{run.input_tokens:,}" if run.input_tokens is not None else "0"
        tout = f"{run.output_tokens:,}" if run.output_tokens is not None else "0"
        return f"| {label} | {calls} | {tin} | {tout} | {cost} | {run.duration_s:.3f} |"

    bases = seeded_manifest.cost_bases() | clean_manifest.cost_bases()
    cost_note = (
        "Cost is notional: the CLI reports it on a list-price basis (`costBasis: list`)."
        if bases == {"list"}
        else f"Cost is as reported by the CLI (`costBasis` values seen: {sorted(map(str, bases))})."
    )
    s1, c1 = ai_seeded_runs[0], ai_clean_runs[0]
    L += [
        "## 5. Calls, tokens, notional cost, duration",
        "",
        "Tokens, cost and duration come from each findings file's `run` block. Call counts come from `judge-manifest.json`.",
        cost_note,
        "",
        "| run | calls | input tokens | output tokens | notional cost (USD) | duration (s) |",
        "|---|---|---|---|---|---|",
        run_row("deterministic, seeded", None, det_seeded_runs[0]),
        run_row("deterministic, clean", None, det_clean_runs[0]),
        run_row(f"AI judge run {_suffix(s1.file_path)}, seeded", seeded_manifest, s1),
        run_row(f"AI judge run {_suffix(c1.file_path)}, clean", clean_manifest, c1),
    ]
    for r in ai_stab_runs:
        L.append(run_row(f"AI judge run {_suffix(r.file_path)}, seeded (repeat)", seeded_manifest, r))
    L.append("")

    e_s = seeded_manifest.entry_for(s1.file_path.name)
    e_c = clean_manifest.entry_for(c1.file_path.name)
    wp_s = seeded_manifest.whole_pass(s1.file_path.name)
    wp_c = clean_manifest.whole_pass(c1.file_path.name)
    if all(e["cache_hits"] > 0 for e in (e_s, e_c)) and all(wp["invocations"] > 1 for wp in (wp_s, wp_c)):
        L += [
            f"**The run-{_suffix(s1.file_path)} `run` blocks understate the real cost.** "
            "Both single runs were resumed after failed attempts,",
            "and they reused cached responses from those attempts. "
            "The `run` block counts only the final invocation's live calls",
            f"(seeded: {e_s['model_calls']} of {e_s['calls']}; clean: {e_c['model_calls']} of {e_c['calls']}). "
            "The cost of reaching each single-run result, summed over the live calls of",
            "every invocation from `calls.json`:",
        ]
    else:
        L += [
            "Cost of reaching each single-run result, summed over the live calls of every invocation "
            "(including failed attempts) from `calls.json`:",
        ]
    L += [
        "",
        "| run | invocations (incl. failed) | live calls | input tokens | output tokens | notional cost (USD) | model time (s) |",
        "|---|---|---|---|---|---|---|",
    ]
    for label, wp in ((f"AI judge run {_suffix(s1.file_path)}, seeded", wp_s),
                      (f"AI judge run {_suffix(c1.file_path)}, clean", wp_c)):
        L.append(
            f"| {label} | {wp['invocations']} | {wp['live']} | {wp['in']:,} | {wp['out']:,} | "
            f"${wp['cost']:.4f} | {wp['dur']:.1f} |"
        )

    mc = [r.cost_usd for r in ai_stab_runs]
    md = [r.duration_s for r in ai_stab_runs]
    mi = [r.input_tokens for r in ai_stab_runs]
    mo = [r.output_tokens for r in ai_stab_runs]
    jobs = stab_entries[0]["calls"]
    L += [
        "",
        f"The {'uncached ' if all_live else ''}repeats give the representative cost of one full AI judge pass "
        f"over {jobs} jobs: "
        f"${min(mc):.3f}-${max(mc):.3f} (mean ${mean(mc):.3f}), {min(md):.0f}-{max(md):.0f} s (mean {mean(md):.0f} s), "
        f"about {mean(mi):,.0f} input and {mean(mo):,.0f} output tokens.",
        "",
        "Deterministic makes no model calls. Its duration is check time only.",
        "Snapshot and screenshot capture (`run.json`: seeded "
        f"{_read_json(args.det_seeded.parent / 'run.json')['duration_s']} s, clean "
        f"{_read_json(args.det_clean.parent / 'run.json')['duration_s']} s) is shared input for "
        + ("deterministic and AI judge." if ex else "both approaches."),
        "It is not charged to either one."
        + (" The AI explorer browses the live app instead and does not use it." if ex else ""),
        "",
    ]
    if ex:
        L += _explorer_cost_section(
            args, ex_seeded_runs[0], ex_clean_runs[0], ex_meta_s1, ex_meta_c1, ex_stab_runs, ex_meta_stab, n_ex_word,
            det_seeded_runs[0], ai_stab_runs, stab_entries, all_live,
        )
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare deterministic, AI judge and (optionally) AI explorer findings for one test run.")
    parser.add_argument("--det-seeded", required=True, type=Path, help="Deterministic findings file, seeded build.")
    parser.add_argument("--det-clean", required=True, type=Path, help="Deterministic findings file, clean build.")
    parser.add_argument("--ai-seeded", required=True, type=Path, help="AI judge single-run findings file, seeded build.")
    parser.add_argument("--ai-clean", required=True, type=Path, help="AI judge single-run findings file, clean build.")
    parser.add_argument("--ai-stability", required=True, type=Path,
                        help="Folder holding only the seeded AI judge repeat findings files.")
    parser.add_argument("--explorer-seeded", type=Path, help="AI explorer single-run findings file, seeded build.")
    parser.add_argument("--explorer-clean", type=Path, help="AI explorer single-run findings file, clean build.")
    parser.add_argument("--explorer-stability", type=Path,
                        help="Folder holding only the complete seeded AI explorer run findings files.")
    parser.add_argument("--out", required=True, type=Path, help="Output Markdown file.")
    args = parser.parse_args(argv)
    if len({args.explorer_seeded is None, args.explorer_clean is None, args.explorer_stability is None}) > 1:
        parser.error("--explorer-seeded, --explorer-clean and --explorer-stability must be given together")

    try:
        text = build_comparison(args)
    except FindingsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
