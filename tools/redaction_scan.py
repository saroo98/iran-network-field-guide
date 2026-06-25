#!/usr/bin/env python3
"""Public-safety redaction scanner for this repository."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
}

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


@dataclass(frozen=True)
class Finding:
    severity: str
    pattern: str
    path: str
    line: int


def import_scheme_pattern() -> str:
    schemes = ["vless", "vmess", "trojan", "ss", "nipovpn", "dns"]
    return r"(?i)\b(" + "|".join(re.escape(item) for item in schemes) + r")://"


HIGH_RISK_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ipv4-like-value", re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")),
    ("uuid-like-value", re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")),
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("profile-import-scheme", re.compile(import_scheme_pattern())),
    ("token-assignment", re.compile(r"(?i)\b(api[_-]?token|access[_-]?token|auth[_-]?key|private[_-]?key)\b\s*[:=]")),
    ("known-private-domain-fragment", re.compile("digi" + "kalla", re.IGNORECASE)),
    ("known-private-provider-fragment", re.compile("hetz" + "ner|up" + "cloud", re.IGNORECASE)),
]

WARNING_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("safety-term", re.compile(r"(?i)\b(cookie|credential|subscription|qr code|private log)\b")),
    ("generic-sensitive-word", re.compile(r"(?i)\b(secret|password)\b")),
]


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def scan_file(root: Path, path: Path) -> list[Finding]:
    rel = str(path.relative_to(root)).replace("\\", "/")
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for name, pattern in HIGH_RISK_PATTERNS:
            if pattern.search(line):
                findings.append(Finding("high", name, rel, line_number))
        for name, pattern in WARNING_PATTERNS:
            if pattern.search(line):
                findings.append(Finding("warning", name, rel, line_number))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan public repo files for high-risk publish blockers.")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")

    findings: list[Finding] = []
    for path in iter_files(root):
        findings.extend(scan_file(root, path))

    high = [finding for finding in findings if finding.severity == "high"]
    warnings = [finding for finding in findings if finding.severity == "warning"]

    print(f"High-risk findings: {len(high)}")
    print(f"Warning findings: {len(warnings)}")
    if high:
        print("")
        print("High-risk file locations:")
        for finding in high:
            print(f"- {finding.path}:{finding.line} [{finding.pattern}]")
    if warnings:
        print("")
        print("Warning file locations:")
        for finding in warnings:
            print(f"- {finding.path}:{finding.line} [{finding.pattern}]")

    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(main())
