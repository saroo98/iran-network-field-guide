#!/usr/bin/env python3
"""Stage-by-stage connectivity probe for owned or authorized hostnames."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import socket
import ssl
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from http.client import HTTPSConnection
from pathlib import Path
from typing import Any


DEFAULT_TIMEOUT = 8.0


@dataclass
class StageResult:
    stage: str
    status: str
    latency_ms: int | None
    detail: Any


@dataclass
class ProbeResult:
    schema: str
    timestamp_utc: str
    route_family: str
    hostname: str
    tcp_port: int
    http_path: str
    isp_operator: str
    region: str
    network_type: str
    client_app: str
    client_version: str
    stages: list[StageResult]
    error_stage: str
    privacy: str


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def validate_hostname(value: str) -> str:
    host = value.strip().lower()
    if not host:
        raise SystemExit("Hostname is required.")
    blocked_prefixes = ["http://", "https://"]
    if any(host.startswith(prefix) for prefix in blocked_prefixes) or "/" in host:
        raise SystemExit("Pass a hostname only, not a URL.")
    if len(host) > 253:
        raise SystemExit("Hostname is too long.")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789.-")
    if any(ch not in allowed for ch in host):
        raise SystemExit("Hostname contains unsupported characters.")
    if "." not in host:
        raise SystemExit("Hostname must contain at least one dot.")
    return host


def validate_path(value: str) -> str:
    if not value.startswith("/"):
        raise SystemExit("HTTP path must start with '/'.")
    if any(ch in value for ch in ("\r", "\n")):
        raise SystemExit("HTTP path cannot contain newlines.")
    return value


def measure(stage: str, func) -> StageResult:  # type: ignore[no-untyped-def]
    started = time.perf_counter()
    try:
        detail = func()
        elapsed = int((time.perf_counter() - started) * 1000)
        return StageResult(stage=stage, status="ok", latency_ms=elapsed, detail=detail)
    except Exception as exc:  # noqa: BLE001 - diagnostic output should keep the failing stage.
        elapsed = int((time.perf_counter() - started) * 1000)
        return StageResult(stage=stage, status="fail", latency_ms=elapsed, detail=f"{type(exc).__name__}: {exc}")


def resolve_dns(hostname: str, port: int) -> dict[str, Any]:
    infos = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    addresses = sorted({item[4][0] for item in infos})
    return {"answers": addresses}


def test_tcp(hostname: str, port: int, timeout: float) -> dict[str, Any]:
    with socket.create_connection((hostname, port), timeout=timeout):
        return {"remote": f"{hostname}:{port}", "connected": True}


def test_tls(hostname: str, port: int, timeout: float) -> dict[str, Any]:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=timeout) as raw_sock:
        with context.wrap_socket(raw_sock, server_hostname=hostname) as tls_sock:
            cert = tls_sock.getpeercert()
            return {
                "remote": f"{hostname}:{port}",
                "protocol": tls_sock.version(),
                "cipher": tls_sock.cipher()[0] if tls_sock.cipher() else None,
                "certificate_subject": cert.get("subject") if isinstance(cert, dict) else None,
            }


def test_http(hostname: str, port: int, path: str, timeout: float) -> dict[str, Any]:
    context = ssl.create_default_context()
    conn = HTTPSConnection(hostname, port=port, timeout=timeout, context=context)
    try:
        conn.request(
            "HEAD",
            path,
            headers={
                "Host": hostname,
                "Accept": "*/*",
                "Connection": "close",
            },
        )
        response = conn.getresponse()
        response.read()
        return {
            "url": f"https://{hostname}{path}",
            "status_code": response.status,
            "server": response.getheader("server"),
        }
    finally:
        conn.close()


def test_http3(hostname: str, path: str, timeout: float) -> dict[str, Any]:
    curl = shutil.which("curl")
    if not curl:
        raise RuntimeError("curl not found")
    url = f"https://{hostname}{path}"
    command = [curl, "--http3-only", "-I", "--max-time", str(int(timeout)), url]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        output = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(output or f"curl exited with {completed.returncode}")
    first_line = completed.stdout.splitlines()[0] if completed.stdout.splitlines() else ""
    return {"url": url, "curl_http3": "ok", "output_first_line": first_line}


def error_stage(stages: list[StageResult]) -> str:
    for stage_name in ("dns", "tcp", "tls", "http"):
        match = next((stage for stage in stages if stage.stage == stage_name), None)
        if match and match.status != "ok":
            return stage_name
    http3 = next((stage for stage in stages if stage.stage == "http3"), None)
    if http3 and http3.status == "fail":
        return "http3"
    return "none"


def write_json(path: Path, result: ProbeResult) -> None:
    path.write_text(json.dumps(asdict(result), indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, result: ProbeResult) -> None:
    rows = []
    for stage in result.stages:
        rows.append(
            {
                "timestamp_utc": result.timestamp_utc,
                "route_family": result.route_family,
                "hostname": result.hostname,
                "isp_operator": result.isp_operator,
                "region": result.region,
                "network_type": result.network_type,
                "client_app": result.client_app,
                "client_version": result.client_version,
                "stage": stage.stage,
                "status": stage.status,
                "latency_ms": stage.latency_ms,
                "error_stage": result.error_stage,
                "detail": json.dumps(stage.detail, sort_keys=True),
            }
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Probe DNS, TCP, TLS, HTTP, and optional HTTP/3 for an authorized hostname.")
    parser.add_argument("--hostname", required=True, help="Owned or authorized hostname. Hostname only, not a URL.")
    parser.add_argument("--port", type=int, default=443, help="TCP port. Defaults to 443.")
    parser.add_argument("--path", default="/", help="HTTPS path for HEAD request. Defaults to '/'.")
    parser.add_argument("--route-family", default="unknown", help="Public-safe route family label.")
    parser.add_argument("--isp-operator", default="unknown", help="Manually entered ISP/operator.")
    parser.add_argument("--region", default="unknown", help="Manually entered region.")
    parser.add_argument("--network-type", choices=["mobile", "fixed", "wifi", "unknown"], default="unknown")
    parser.add_argument("--client-app", default="unknown", help="Client app name.")
    parser.add_argument("--client-version", default="unknown", help="Client app version.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-stage timeout in seconds.")
    parser.add_argument("--test-http3", action="store_true", help="Attempt HTTP/3 with local curl support.")
    parser.add_argument("--json-out", type=Path, help="Optional JSON output path.")
    parser.add_argument("--csv-out", type=Path, help="Optional CSV output path.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    hostname = validate_hostname(args.hostname)
    path = validate_path(args.path)
    if not 1 <= args.port <= 65535:
        raise SystemExit("Port must be between 1 and 65535.")

    stages = [
        measure("dns", lambda: resolve_dns(hostname, args.port)),
        measure("tcp", lambda: test_tcp(hostname, args.port, args.timeout)),
        measure("tls", lambda: test_tls(hostname, args.port, args.timeout)),
        measure("http", lambda: test_http(hostname, args.port, path, args.timeout)),
    ]
    if args.test_http3:
        stages.append(measure("http3", lambda: test_http3(hostname, path, args.timeout)))
    else:
        stages.append(StageResult("http3", "not_tested", None, "Use --test-http3 to run this stage."))

    result = ProbeResult(
        schema="iran-network-field-guide-connectivity-probe-v1",
        timestamp_utc=utc_timestamp(),
        route_family=args.route_family,
        hostname=hostname,
        tcp_port=args.port,
        http_path=path,
        isp_operator=args.isp_operator,
        region=args.region,
        network_type=args.network_type,
        client_app=args.client_app,
        client_version=args.client_version,
        stages=stages,
        error_stage=error_stage(stages),
        privacy="No packet captures, browsing history, account identifiers, client import material, cookies, or credential values are collected.",
    )

    print(json.dumps(asdict(result), indent=2, sort_keys=True))
    if args.json_out:
        write_json(args.json_out, result)
    if args.csv_out:
        write_csv(args.csv_out, result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
