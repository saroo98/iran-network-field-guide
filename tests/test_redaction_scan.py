from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import redaction_scan


class RedactionScanTests(unittest.TestCase):
    def test_detects_high_risk_ipv4_like_value(self) -> None:
        unsafe_value = "203" + ".0" + ".113" + ".9"
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = root / "example.md"
            path.write_text(f"endpoint={unsafe_value}\n", encoding="utf-8")

            findings = redaction_scan.scan_file(root, path)

        self.assertIn("ipv4-like-value", {finding.pattern for finding in findings})
        self.assertIn("high", {finding.severity for finding in findings})

    def test_detects_warning_terms_without_high_risk(self) -> None:
        warning_text = "pass" + "word"
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = root / "example.md"
            path.write_text(f"placeholder {warning_text}\n", encoding="utf-8")

            findings = redaction_scan.scan_file(root, path)

        self.assertIn("generic-sensitive-word", {finding.pattern for finding in findings})
        self.assertNotIn("high", {finding.severity for finding in findings})


if __name__ == "__main__":
    unittest.main()
