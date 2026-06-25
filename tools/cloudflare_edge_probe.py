#!/usr/bin/env python3
"""Probe explicit CDN edge candidates for an owned Cloudflare-backed hostname."""

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import socket
import ssl
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


MAX_IPS = 20
DEFAULT_TIMEOUT = 8.0
MAX_HEADER_BYTES = 16384


@dataclass
class EdgeResult:
    ip: str
    hostname: str
    port: int
    path: str
    tcp_ok: bool
    tls_ok: bool
    http_ok: bool
    status_code: int | None
    elapsed_ms: int
    error_stage: str
    error: str | None


def validate_hostname(value: str) -> str:
    host = value.strip().lower()
    if not host or "://" in host or "/" in host:
        raise SystemExit("Pass a hostname only, not a URL.")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789.-")
    if any(ch not in allowed for ch in host) or "." not in host:
        raise SystemExit("Hostname contains unsupported characters.")
    return host


def parse_ip_list(values: Iterable[str]) -> list[str]:
    ips: list[str] = []
    for value in values:
        for part in value.replace(",", " ").split():
            candidate = part.strip()
            if not candidate:
                continue
            if "/" in candidate:
                raise SystemExit("CIDR ranges are refused. Provide explicit IP candidates only.")
            try:
                parsed = ipaddress.ip_address(candidate)
            except ValueError as exc:
                raise SystemExit(f"Invalid IP address: {candidate}") from exc
            ips.append(str(parsed))
    if not ips:
        raise SystemExit("Provide at least one --ip value.")
    if len(ips) > MAX_IPS:
        raise SystemExit(f"Refusing to test more than {MAX_IPS} IPs in one run.")
    return ips


def validate_path(value: str) -> str:
    if not value.startswith("/"):
        raise SystemExit("Path must start with '/'.")
    if any(ch in value for ch in ("\r", "\n")):
        raise SystemExit("Path cannot contain newlines.")
    return value


def parse_status_code(header_bytes: bytes) -> int | None:
    first_line = header_bytes.decode("iso-8859-1", errors="replace").splitlines()[0:1]
    if not first_line:
        return None
    parts = first_line[0].split()
    if len(parts) < 2:
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


def probe_one(ip: str, hostname: str, path: str, port: int, timeout: float) -> EdgeResult:
    started = time.perf_counter()
    tcp_ok = False
    tls_ok = False
    http_ok = False
    status_code: int | None = None
    error_stage = "none"
    error: str | None = None

    try:
        raw_sock = socket.create_connection((ip, port), timeout=timeout)
        tcp_ok = True
    except OSError as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return EdgeResult(ip, hostname, port, path, tcp_ok, tls_ok, http_ok, status_code, elapsed_ms, "tcp", str(exc))

    try:
        context = ssl.create_default_context()
        with context.wrap_socket(raw_sock, server_hostname=hostname) as tls_sock:
            tls_ok = True
            request = (
                f"HEAD {path} HTTP/1.1\r\n"
                f"Host: {hostname}\r\n"
                "Accept: */*\r\n"
                "Connection: close\r\n\r\n"
            )
            tls_sock.sendall(request.encode("ascii"))
            chunks: list[bytes] = []
            total = 0
            while total < MAX_HEADER_BYTES:
                chunk = tls_sock.recv(1024)
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if b"\r\n\r\n" in b"".join(chunks):
                    break
            header_bytes = b"".join(chunks)
            status_code = parse_status_code(header_bytes)
            http_ok = status_code is not None
            if not http_ok:
                error_stage = "http"
                error = "No HTTP status line received."
    except ssl.SSLError as exc:
        error_stage = "tls"
        error = str(exc)
    except OSError as exc:
        error_stage = "http"
        error = str(exc)
    except Exception as exc:  # noqa: BLE001 - diagnostic tool preserves unexpected stage.
        error_stage = "http"
        error = f"{type(exc).__name__}: {exc}"

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    if error_stage == "none" and not tls_ok:
        error_stage = "tls"
    if error_stage == "none" and not http_ok:
        error_stage = "http"
    return EdgeResult(ip, hostname, port, path, tcp_ok, tls_ok, http_ok, status_code, elapsed_ms, error_stage, error)


def write_json(path: Path, rows: list[EdgeResult]) -> None:
    payload = {
        "schema": "iran-network-field-guide-cdn-edge-probe-v1",
        "privacy": "No packet captures, browsing history, account identifiers, client import material, cookies, or credential values are collected.",
        "results": [asdict(row) for row in rows],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[EdgeResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe explicit CDN edge IP candidates for one owned hostname.")
    parser.add_argument("--hostname", required=True, help="Owned CDN-backed hostname. Hostname only.")
    parser.add_argument("--ip", action="append", default=[], help="Explicit IP candidate. Repeat or pass comma-separated values.")
    parser.add_argument("--path", default="/", help="HTTPS path for HEAD request.")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--csv-out", type=Path)
    args = parser.parse_args()

    hostname = validate_hostname(args.hostname)
    path = validate_path(args.path)
    if not 1 <= args.port <= 65535:
        raise SystemExit("Port must be between 1 and 65535.")
    ips = parse_ip_list(args.ip)
    rows = [probe_one(ip, hostname, path, args.port, args.timeout) for ip in ips]
    print(json.dumps([asdict(row) for row in rows], indent=2, sort_keys=True))
    if args.json_out:
        write_json(args.json_out, rows)
    if args.csv_out:
        write_csv(args.csv_out, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
