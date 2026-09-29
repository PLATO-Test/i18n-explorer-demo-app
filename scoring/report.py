"""Builds one results dict from scored runs, then renders it as JSON and
Markdown - both come from the same dict so they can't drift."""
from collections import defaultdict
from statistics import mean

from scoring.findings import Run
from scoring.ground_truth import Entry, KnownIssue
from scoring.matcher import RunResult, score_run

LAYERS = ("deterministic", "ai", "both")


def _finding_ref(rr: RunResult, idx: int) -> dict:
    f = rr.run.findings[idx]
    return {
        "run_id": rr.run.run_id,
        "page_path": f.page_path,
        "data_testid": f.data_testid,
        "observed": f.observed,
        "category": f.category,
    }


def _source_report(source: str, results: list[RunResult], defects: list[Entry], build: str) -> dict:
    n_runs = len(results)
    defects_by_id = {d.id: d for d in defects}

    stability: dict[str, int] = {d.id: 0 for d in defects}
    matched_refs: dict[str, list[dict]] = defaultdict(list)
    category_correct: dict[str, bool] = {}
    per_run_recall: list[float] = []
    per_run_precision: list[float | None] = []
    control_fp_total: dict[str, int] = defaultdict(int)
    control_fp_refs: dict[str, list[dict]] = defaultdict(list)
    known_issue_total: dict[str, int] = defaultdict(int)
    known_issue_refs: dict[str, list[dict]] = defaultdict(list)
    unclassified_refs: list[dict] = []

    for rr in results:
        detected_ids = set(rr.detected)
        for did, idxs in rr.detected.items():
            stability[did] += 1
            for idx in idxs:
                matched_refs[did].append(_finding_ref(rr, idx))
                if rr.run.findings[idx].category == defects_by_id[did].category:
                    category_correct[did] = True
            category_correct.setdefault(did, False)

        for cid, idxs in rr.control_fp.items():
            control_fp_total[cid] += len(idxs)
            for idx in idxs:
                control_fp_refs[cid].append(_finding_ref(rr, idx))

        for kid, idxs in rr.known_issue.items():
            known_issue_total[kid] += len(idxs)
            for idx in idxs:
                known_issue_refs[kid].append(_finding_ref(rr, idx))

        for idx in rr.unclassified:
            unclassified_refs.append(_finding_ref(rr, idx))

        n_findings = len(rr.run.findings)
        known_issue_count = sum(len(v) for v in rr.known_issue.values())
        if build == "seeded":
            per_run_recall.append(len(detected_ids) / len(defects) if defects else 0.0)
            matched_count = sum(len(v) for v in rr.detected.values())
            denom = n_findings - known_issue_count
            per_run_precision.append(matched_count / denom if denom else None)
        else:
            per_run_precision.append(None)

    defect_table = None
    layer_breakdown = None
    recall = None
    if build == "seeded":
        defect_table = [
            {
                "id": d.id,
                "detected": stability[d.id] > 0,
                "matched_findings": matched_refs.get(d.id, []),
                "category_correct": category_correct.get(d.id),
            }
            for d in defects
        ]
        layer_breakdown = {layer: {"detected": 0, "missed": 0} for layer in LAYERS}
        for d in defects:
            bucket = "detected" if stability[d.id] > 0 else "missed"
            layer_breakdown[d.expected_layer][bucket] += 1
        recall = mean(per_run_recall) if per_run_recall else None

    precisions = [p for p in per_run_precision if p is not None]
    precision = mean(precisions) if precisions else None

    run_meta = [
        {
            "run_id": rr.run.run_id,
            "model": rr.run.model,
            "input_tokens": rr.run.input_tokens,
            "output_tokens": rr.run.output_tokens,
            "cost_usd": rr.run.cost_usd,
            "duration_s": rr.run.duration_s,
        }
        for rr in results
    ]

    def _sum_or_none(key: str):
        vals = [m[key] for m in run_meta if m[key] is not None]
        return sum(vals) if vals else None

    return {
        "n_runs": n_runs,
        "defect_table": defect_table,
        "layer_breakdown": layer_breakdown,
        "control_false_positives": [
            {"control_id": cid, "count": count, "findings": control_fp_refs[cid]}
            for cid, count in sorted(control_fp_total.items())
        ],
        "known_issues": [
            {"issue_id": kid, "count": count, "findings": known_issue_refs[kid]}
            for kid, count in sorted(known_issue_total.items())
        ],
        "unclassified": unclassified_refs,
        "precision": precision,
        "recall": recall,
        "false_positive_count": sum(control_fp_total.values()) + len(unclassified_refs),
        "stability": (
            {did: {"detected_runs": k, "total_runs": n_runs} for did, k in sorted(stability.items())}
            if n_runs > 1 and build == "seeded"
            else None
        ),
        "cost": {
            "total_cost_usd": _sum_or_none("cost_usd"),
            "total_input_tokens": _sum_or_none("input_tokens"),
            "total_output_tokens": _sum_or_none("output_tokens"),
            "mean_duration_s": mean(m["duration_s"] for m in run_meta) if run_meta else None,
            "models": sorted({m["model"] for m in run_meta if m["model"] is not None}),
        },
        "runs": run_meta,
    }


def build_report(
    runs: list[Run],
    defects: list[Entry],
    controls: list[Entry],
    build: str,
    known_issues: list[KnownIssue] = (),
) -> dict:
    by_source: dict[str, list[Run]] = defaultdict(list)
    for r in runs:
        by_source[r.source].append(r)

    sources = {}
    for source, source_runs in by_source.items():
        results = [score_run(r, defects, controls, build, known_issues) for r in source_runs]
        sources[source] = _source_report(source, results, defects, build)

    return {"build": build, "n_defects": len(defects), "sources": sources}


def _fmt(v, digits: int = 3) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        return f"{v:.{digits}f}"
    return str(v)


def render_markdown(report: dict) -> str:
    lines = [f"# Scoring report - {report['build']} build", ""]
    for source, sr in report["sources"].items():
        lines.append(f"## {source} ({sr['n_runs']} run{'s' if sr['n_runs'] != 1 else ''})")
        lines.append("")

        if sr["layer_breakdown"] is not None:
            lines.append("### Detected / missed by expected layer")
            lines.append("")
            lines.append("| layer | detected | missed |")
            lines.append("|---|---|---|")
            for layer in LAYERS:
                lb = sr["layer_breakdown"][layer]
                lines.append(f"| {layer} | {lb['detected']} | {lb['missed']} |")
            lines.append("")

        if sr["defect_table"] is not None:
            lines.append("### Per-defect")
            lines.append("")
            lines.append("| id | detected | category correct | matched findings |")
            lines.append("|---|---|---|---|")
            for row in sr["defect_table"]:
                refs = "; ".join(
                    f"{m['run_id']}:{m['page_path']}#{m['data_testid']}" for m in row["matched_findings"]
                ) or "-"
                lines.append(
                    f"| {row['id']} | {'yes' if row['detected'] else 'no'} | "
                    f"{'yes' if row['category_correct'] else ('no' if row['detected'] else 'n/a')} | {refs} |"
                )
            lines.append("")

        if sr["stability"] is not None:
            lines.append("### Stability")
            lines.append("")
            lines.append("| id | detected runs | total runs |")
            lines.append("|---|---|---|")
            for did, s in sr["stability"].items():
                lines.append(f"| {did} | {s['detected_runs']} | {s['total_runs']} |")
            lines.append("")

        lines.append("### False positives on controls")
        lines.append("")
        if sr["control_false_positives"]:
            lines.append("| control id | count |")
            lines.append("|---|---|")
            for fp in sr["control_false_positives"]:
                lines.append(f"| {fp['control_id']} | {fp['count']} |")
        else:
            lines.append("None.")
        lines.append("")

        lines.append("### Known issues (not counted toward recall or false positives)")
        lines.append("")
        if sr["known_issues"]:
            lines.append("| known-issue id | count |")
            lines.append("|---|---|")
            for ki in sr["known_issues"]:
                lines.append(f"| {ki['issue_id']} | {ki['count']} |")
        else:
            lines.append("None.")
        lines.append("")

        lines.append("### Unclassified findings (manual review)")
        lines.append("")
        if sr["unclassified"]:
            lines.append("| run | page | testid | observed |")
            lines.append("|---|---|---|---|")
            for u in sr["unclassified"]:
                lines.append(f"| {u['run_id']} | {u['page_path']} | {u['data_testid']} | {u['observed']} |")
        else:
            lines.append("None.")
        lines.append("")

        lines.append("### Precision / recall")
        lines.append("")
        lines.append(f"- precision: {_fmt(sr['precision'])}")
        lines.append(f"- recall: {_fmt(sr['recall'])}")
        lines.append(f"- false positive count: {sr['false_positive_count']}")
        lines.append("")

        lines.append("### Cost / tokens / duration")
        lines.append("")
        c = sr["cost"]
        lines.append(f"- total cost (USD): {_fmt(c['total_cost_usd'])}")
        lines.append(f"- total input tokens: {_fmt(c['total_input_tokens'], 0)}")
        lines.append(f"- total output tokens: {_fmt(c['total_output_tokens'], 0)}")
        lines.append(f"- mean duration (s): {_fmt(c['mean_duration_s'])}")
        lines.append(f"- models: {', '.join(c['models']) or 'n/a'}")
        lines.append("")

    return "\n".join(lines)
