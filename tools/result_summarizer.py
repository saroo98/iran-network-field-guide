#!/usr/bin/env python3
"""Summarize sanitized probe JSON or CSV files into Markdown."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return payload["results"]
    if isinstance(payload, dict):
        return [payload]
    raise ValueError(f"Unsupported JSON shape: {path}")


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        suffix = path.suffix.lower()
        if suffix == ".json":
            rows.extend(load_json(path))
        elif suffix == ".csv":
            rows.extend(load_csv(path))
        else:
            raise ValueError(f"Unsupported input file type: {path}")
    return rows


def flatten(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    flattened: list[dict[str, str]] = []
    for row in rows:
        base = {
            "timestamp_utc": str(row.get("timestamp_utc", "unknown")),
            "route_family": str(row.get("route_family", "unknown")),
            "hostname": str(row.get("hostname", "unknown")),
            "isp_operator": str(row.get("isp_operator", "unknown")),
            "region": str(row.get("region", "unknown")),
            "network_type": str(row.get("network_type", "unknown")),
            "client_app": str(row.get("client_app", "unknown")),
            "client_version": str(row.get("client_version", "unknown")),
            "error_stage": str(row.get("error_stage", "unknown")),
            "failure_label": str(row.get("failure_label", row.get("error_stage", "unknown"))),
        }
        stages = row.get("stages")
        if isinstance(stages, list):
            for stage in stages:
                if isinstance(stage, dict):
                    item = dict(base)
                    item["stage"] = str(stage.get("stage", "unknown"))
                    item["status"] = str(stage.get("status", "unknown"))
                    item["latency_ms"] = str(stage.get("latency_ms", ""))
                    flattened.append(item)
        elif "stage" in row:
            item = dict(base)
            item["stage"] = str(row.get("stage", "unknown"))
            item["status"] = str(row.get("status", "unknown"))
            item["latency_ms"] = str(row.get("latency_ms", ""))
            flattened.append(item)
        else:
            item = dict(base)
            item["stage"] = "aggregate"
            item["status"] = "ok" if row.get("error_stage") in (None, "none") else "fail"
            item["latency_ms"] = str(row.get("elapsed_ms", ""))
            flattened.append(item)
    return flattened


def markdown_summary(rows: list[dict[str, str]]) -> str:
    by_context: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    by_stage: dict[str, Counter[str]] = defaultdict(Counter)
    failures = Counter()

    for row in rows:
        context = (
            row.get("route_family", "unknown"),
            row.get("isp_operator", "unknown"),
            row.get("network_type", "unknown"),
            row.get("error_stage", "unknown"),
        )
        by_context[context][row.get("status", "unknown")] += 1
        by_stage[row.get("stage", "unknown")][row.get("status", "unknown")] += 1
        failures[row.get("failure_label", "unknown")] += 1

    lines = [
        "# Sanitized Probe Summary",
        "",
        f"Rows summarized: {len(rows)}",
        "",
        "## By Route, ISP, Network, And Error Stage",
        "",
        "| Route family | ISP/operator | Network | Error stage | Status counts |",
        "|---|---|---|---|---|",
    ]
    for (route_family, isp, network, error_stage), counts in sorted(by_context.items()):
        count_text = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        lines.append(f"| {route_family} | {isp} | {network} | {error_stage} | {count_text} |")

    lines.extend(["", "## By Stage", "", "| Stage | Status counts |", "|---|---|"])
    for stage, counts in sorted(by_stage.items()):
        count_text = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        lines.append(f"| {stage} | {count_text} |")

    lines.extend(["", "## Failure Labels", "", "| Label | Count |", "|---|---:|"])
    for label, count in sorted(failures.items()):
        lines.append(f"| {label} | {count} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize sanitized probe JSON/CSV outputs.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, help="Optional Markdown output path.")
    args = parser.parse_args()

    rows = flatten(load_rows(args.inputs))
    output = markdown_summary(rows)
    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
