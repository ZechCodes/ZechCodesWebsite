"""Container trust regression checks; run directly with Python's stdlib."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContainerTrustTests(unittest.TestCase):
    def test_installer_uses_current_trust(self):
        dockerfile = (ROOT / "Dockerfile").read_text()
        self.assertIn("ghcr.io/astral-sh/uv:0.13.4", dockerfile)
        self.assertIn("certifi==2026.10.19", dockerfile)
        self.assertIn("verify_ca_trust.py", dockerfile)

    def test_both_stages_use_supported_debian(self):
        stages = [line for line in (ROOT / "Dockerfile").read_text().splitlines() if line.startswith("FROM python:")]
        self.assertEqual(len(stages), 2)
        self.assertTrue(all("3.11-slim-bookworm" in stage for stage in stages))



if __name__ == "__main__":
    unittest.main()
