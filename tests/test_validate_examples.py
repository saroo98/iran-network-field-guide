from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import validate_examples


class ValidateExamplesTests(unittest.TestCase):
    def test_accepts_committed_sanitized_examples(self) -> None:
        repo = Path(__file__).resolve().parents[1]

        errors = []
        for path in validate_examples.collect_files([repo / "data" / "examples"]):
            errors.extend(validate_examples.validate_file(path))

        self.assertEqual([], errors)

    def test_rejects_unknown_stage(self) -> None:
        row = self.valid_row()
        row["stages"][0]["stage"] = "mystery"

        errors = validate_examples.validate_result(row, "memory:1")

        self.assertTrue(any("unknown stage mystery" in error for error in errors))

    def test_rejects_url_shaped_values(self) -> None:
        row = self.valid_row()
        row["hostname"] = "https" + "://example.invalid"

        errors = validate_examples.validate_result(row, "memory:1")

        self.assertTrue(any("url-like-value" in error for error in errors))

    def test_rejects_missing_required_field_from_file(self) -> None:
        row = self.valid_row()
        del row["route_family"]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.json"
            path.write_text(json.dumps({"results": [row]}), encoding="utf-8")

            errors = validate_examples.validate_file(path)

        self.assertTrue(any("missing field route_family" in error for error in errors))

    @staticmethod
    def valid_row() -> dict[str, object]:
        return {
            "timestamp_utc": "2026-06-25T00:00:00Z",
            "route_family": "WebSocket/TLS CDN",
            "hostname": "EXAMPLE_HOSTNAME",
            "isp_operator": "EXAMPLE_ISP",
            "region": "EXAMPLE_REGION",
            "network_type": "mobile",
            "client_app": "EXAMPLE_CLIENT_NAME",
            "client_version": "EXAMPLE_VERSION",
            "stages": [
                {
                    "stage": "dns",
                    "status": "ok",
                    "latency_ms": 12,
                }
            ],
            "error_stage": "none",
            "failure_label": "works",
        }


if __name__ == "__main__":
    unittest.main()
