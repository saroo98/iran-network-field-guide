#!/usr/bin/env python3
"""Validate public-safe example result files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ALLOWED_STAGES = {"dns", "tcp", "tls", "http", "http3", "udp", "proxy", "app"}
ALLOWED_STATUSES = {"ok", "fail", "not_tested"}
ALLOWED_NETWORK_TYPES = {"mobile", "fixed", "wifi", "unknown"}
ALLOWED_FAILURE_LABELS = {
    "dns-fail",
    "tcp-fail",
    "tls-fail",
    "http-fail",
    "udp-fail",
    "proxy-fail",
    "upload-stall",
    "grey-connect",
    "random-reset",
    "client-import",
    "works",
}
REQUIRED_CONTEXT_FIELDS = {
    "timestamp_utc",
    "route_family",
    "hostname",
    "isp_operator",
    "region",
    "network_type",
    "client_app",
    "client_version",
    "error_stage",
    "failure_label",
}
REQUIRED_STAGE_FIELDS = {"stage", "status", "latency_ms"}
RISK_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ipv4-like-value", re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")),
    ("url-like-value", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://")),
]


def collect_files(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(item for item in path.rglob("*") if item.suffix.lower() in {".json", ".csv"}))
        elif path.suffix.lower() in {".json", ".csv"}:
            files.append(path)
        else:
            raise ValueError(f"Unsupported input path: {path}")
    return files


def load_json(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict) and isinstance(payload.get("results"), list):
        rows = payload["results"]
    elif isinstance(payload, dict):
        rows = [payload]
    else:
        raise ValueError(f"{path}: unsupported JSON shape")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: JSON results must be objects")
    return rows


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def walk_strings(value: Any, location: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield location, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{location}[{index}]")


def require_fields(row: dict[str, Any], required: set[str], context: str) -> list[str]:
    return [f"{context}: missing field {field}" for field in sorted(required) if field not in row or row[field] in (None, "")]


def validate_latency(value: Any, status: str, context: str) -> list[str]:
    if status == "not_tested" and value in (None, ""):
        return []
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return [f"{context}: latency_ms must be an integer or blank when not tested"]
    if parsed < 0:
        return [f"{context}: latency_ms cannot be negative"]
    return []


def validate_hostname(value: Any, context: str) -> list[str]:
    hostname = str(value)
    if hostname != "EXAMPLE_HOSTNAME":
        return [f"{context}: hostname must be EXAMPLE_HOSTNAME"]
    return []


def validate_risky_values(row: dict[str, Any], context: str) -> list[str]:
    errors: list[str] = []
    for location, value in walk_strings(row):
        for name, pattern in RISK_PATTERNS:
            if pattern.search(value):
                errors.append(f"{context}{location[1:]}: rejected {name}")
    return errors


def validate_stage(stage: dict[str, Any], context: str) -> list[str]:
    errors = require_fields(stage, REQUIRED_STAGE_FIELDS - {"latency_ms"}, context)
    if "latency_ms" not in stage:
        errors.append(f"{context}: missing field latency_ms")
    stage_name = str(stage.get("stage", ""))
    status = str(stage.get("status", ""))
    if stage_name and stage_name not in ALLOWED_STAGES:
        errors.append(f"{context}: unknown stage {stage_name}")
    if status and status not in ALLOWED_STATUSES:
        errors.append(f"{context}: unknown status {status}")
    if "latency_ms" in stage:
        errors.extend(validate_latency(stage.get("latency_ms"), status, context))
    return errors


def validate_result(row: dict[str, Any], context: str) -> list[str]:
    errors = require_fields(row, REQUIRED_CONTEXT_FIELDS, context)
    errors.extend(validate_risky_values(row, context))
    if "hostname" in row:
        errors.extend(validate_hostname(row["hostname"], context))
    network_type = str(row.get("network_type", ""))
    if network_type and network_type not in ALLOWED_NETWORK_TYPES:
        errors.append(f"{context}: unknown network_type {network_type}")
    error_stage = str(row.get("error_stage", ""))
    if error_stage and error_stage != "none" and error_stage not in ALLOWED_STAGES:
        errors.append(f"{context}: unknown error_stage {error_stage}")
    failure_label = str(row.get("failure_label", ""))
    if failure_label and failure_label not in ALLOWED_FAILURE_LABELS:
        errors.append(f"{context}: unknown failure_label {failure_label}")

    stages = row.get("stages")
    if isinstance(stages, list):
        if not stages:
            errors.append(f"{context}: stages cannot be empty")
        for index, stage in enumerate(stages):
            if not isinstance(stage, dict):
                errors.append(f"{context}.stages[{index}]: stage must be an object")
                continue
            errors.extend(validate_stage(stage, f"{context}.stages[{index}]"))
    elif "stage" in row:
        errors.extend(validate_stage(row, context))
    else:
        errors.append(f"{context}: missing stages list or flattened stage field")
    return errors


def validate_file(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    rows = load_json(path) if suffix == ".json" else load_csv(path)
    errors: list[str] = []
    for index, row in enumerate(rows, start=1):
        errors.extend(validate_result(row, f"{path}:{index}"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sanitized example JSON and CSV files.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    for path in collect_files(args.paths):
        try:
            errors.extend(validate_file(path))
        except Exception as exc:  # noqa: BLE001 - validation CLI reports file-specific parse errors.
            errors.append(f"{path}: {type(exc).__name__}: {exc}")

    if errors:
        print("Example validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Example validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
