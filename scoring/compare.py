"""Comparison CLI: deterministic (phase 1) vs AI judge (phase 2) findings
for one test run, written as a single Markdown report.

    uv run python -m scoring.compare \\
        --det-seeded <run>/seeded/findings.json --det-clean <run>/clean/findings.json \\
        --ai-seeded <run>/seeded/findings-ai-judge-1.json --ai-clean <run>/clean/findings-ai-judge-1.json \\
        --ai-stability <folder of seeded AI judge repeats> --out <comparison.md>

Call counts come from judge-manifest.json next to --ai-seeded / --ai-clean,
and snapshot capture time from run.json next to --det-seeded / --det-clean.
Stability files are looked up by file name in the seeded manifest, so a
folder of copies works as long as the names are unchanged.

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
from scoring.ground_truth import Entry, load_controls, load_defects
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


def _score(path: Path, build: str, defects: list[Entry], controls: list[Entry]) -> tuple[dict, list[Run]]:
    runs = load_runs(path)
    if not runs:
        raise SystemExit(f"No findings files found at {path}")
    report = build_report(runs, defects, controls, build)
    if len(report["sources"]) != 1:
        raise SystemExit(f"{path}: expected one findings source, got {sorted(report['sources'])}")
    return next(iter(report["sources"].values())), runs


def _detected(sr: dict) -> dict[str, bool]:
    return {row["id"]: row["detected"] for row in sr["defect_table"]}


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


def build_comparison(args: argparse.Namespace) -> str:
    defects = load_defects()
    controls = load_controls()

    det_seeded, det_seeded_runs = _score(args.det_seeded, "seeded", defects, controls)
    det_clean, det_clean_runs = _score(args.det_clean, "clean", defects, controls)
    ai_seeded, ai_seeded_runs = _score(args.ai_seeded, "seeded", defects, controls)
    ai_clean, ai_clean_runs = _score(args.ai_clean, "clean", defects, controls)
    ai_stab, ai_stab_runs = _score(args.ai_stability, "seeded", defects, controls)
    if len(ai_stab_runs) < 2:
        raise SystemExit(f"--ai-stability needs at least 2 runs, found {len(ai_stab_runs)} in {args.ai_stability}")
    n_rep = len(ai_stab_runs)
    n_rep_word = NUMBER_WORDS.get(n_rep, str(n_rep))

    seeded_manifest = Manifest(args.ai_seeded.parent)
    clean_manifest = Manifest(args.ai_clean.parent)

    det = _detected(det_seeded)
    ai = _detected(ai_seeded)
    union = {d.id: det[d.id] or ai[d.id] for d in defects}
    n = len(defects)

    inputs = [args.det_seeded, args.det_clean, args.ai_seeded, args.ai_clean]
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
    L += [
        f"# Phase 1 vs phase 2 comparison - run {ai_seeded_runs[0].run_id}",
        "",
        f"Inputs (all under `{base_shown}/`):",
        "",
        f"- Phase 1 deterministic: `{rel(args.det_seeded)}`, `{rel(args.det_clean)}`",
        f"- Phase 2 AI judge, single run: `{rel(args.ai_seeded)}`, `{rel(args.ai_clean)}`",
        f"- Phase 2 AI judge, stability: {stab_shown} (seeded only, no clean repeats)",
        "",
        "All inputs were scored in memory with `scoring.report.build_report`, the same code behind `scoring.score`.",
        f"The \"AI judge\" columns in sections 1-3 are single run {_suffix(args.ai_seeded)}. "
        "Repeats appear only in section 4.",
        "",
    ]

    # 1. Per-defect
    L += [
        "## 1. Per-defect detection (seeded build)",
        "",
        "| id | category | expected_layer | deterministic | AI judge | union |",
        "|---|---|---|---|---|---|",
    ]
    for d in defects:
        L.append(f"| {d.id} | {d.category} | {d.expected_layer} | {_yn(det[d.id])} | {_yn(ai[d.id])} | {_yn(union[d.id])} |")
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
    for name, hits in (("deterministic", det), ("AI judge", ai), ("union", union)):
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

    approaches = (
        ("deterministic", "Deterministic", det_seeded, det_seeded_runs, det_clean, det_clean_runs),
        (f"AI judge (run {_suffix(args.ai_seeded)})", f"AI judge (run {_suffix(args.ai_seeded)})",
         ai_seeded, ai_seeded_runs, ai_clean, ai_clean_runs),
    )
    L += [
        "## 3. False positives",
        "",
        "On the seeded build a finding is a false positive only if it lands on a control (a correct element).",
        "Findings that match neither a defect nor a control are \"unclassified\" and need manual review.",
        "On the clean build nothing is wrong, so every finding is a false positive.",
        "",
        "| approach | seeded: control FPs | seeded: unclassified | seeded: total findings | clean: findings (all FP) |",
        "|---|---|---|---|---|",
    ]
    for name, _, s_sr, s_runs, _, c_runs in approaches:
        ctrl = sum(fp["count"] for fp in s_sr["control_false_positives"])
        L.append(
            f"| {name} | {ctrl} | {len(s_sr['unclassified'])} | {sum(len(r.findings) for r in s_runs)} | "
            f"{sum(len(r.findings) for r in c_runs)} |"
        )
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

    # 4. Stability
    stab_entries = [seeded_manifest.entry_for(p.name) for p in stab_files]
    all_live = all(e.get("cache") == "bypassed" and e["model_calls"] == e["calls"] for e in stab_entries)
    stab_names = stab_files[0].stem.rsplit("-", 1)[0] + "-" + "/".join(_suffix(p) for p in stab_files) + ".json"
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
        sum(row["detected"] for row in build_report([r], defects, controls, "seeded")["sources"]["ai_judge"]["defect_table"])
        for r in ai_stab_runs
    ]
    L += [
        "",
        f"Defects detected per repeat: {', '.join(f'{k}/{n}' for k in per_run)}; "
        f"mean recall {ai_stab['recall']:.3f}.",
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
        f"{_read_json(args.det_clean.parent / 'run.json')['duration_s']} s) is shared input for both approaches.",
        "It is not charged to either one.",
        "",
    ]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare deterministic and AI judge findings for one test run.")
    parser.add_argument("--det-seeded", required=True, type=Path, help="Deterministic findings file, seeded build.")
    parser.add_argument("--det-clean", required=True, type=Path, help="Deterministic findings file, clean build.")
    parser.add_argument("--ai-seeded", required=True, type=Path, help="AI judge single-run findings file, seeded build.")
    parser.add_argument("--ai-clean", required=True, type=Path, help="AI judge single-run findings file, clean build.")
    parser.add_argument("--ai-stability", required=True, type=Path,
                        help="Folder holding only the seeded AI judge repeat findings files.")
    parser.add_argument("--out", required=True, type=Path, help="Output Markdown file.")
    args = parser.parse_args(argv)

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
