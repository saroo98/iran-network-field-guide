from __future__ import annotations

import unittest
from pathlib import Path

from tools import result_summarizer


class ResultSummarizerTests(unittest.TestCase):
    def test_summarizes_existing_and_scenario_examples(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        inputs = [
            repo / "data" / "examples" / "sanitized-results.json",
            repo / "data" / "examples" / "sanitized-scenarios.json",
        ]

        rows = result_summarizer.flatten(result_summarizer.load_rows(inputs))
        output = result_summarizer.markdown_summary(rows)

        self.assertIn("# Sanitized Probe Summary", output)
        self.assertIn("Rows summarized:", output)
        self.assertIn("dns-fail", output)
        self.assertIn("client-import", output)
        self.assertIn("works", output)


if __name__ == "__main__":
    unittest.main()
