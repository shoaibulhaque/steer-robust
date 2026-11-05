"""Behavior tests for the local audit helper; no model calls or dependencies."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "package/.agents/skills/project-exploration/scripts/inspect_guidance.py")
FIXTURE = """# Root
Overview.
## Retry
Check UNKNOWN outcomes first.
**Exception:** safe known refusal.
```md
```example
## This is an example, not a section
```
## Other
Unrelated.
"""


class InspectionFixture:
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="steer-inspect-test-")
        self.addCleanup(self.directory.cleanup)
        (Path(self.directory.name) / "fixture.md").write_text(FIXTURE)

    def run_helper(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), self.directory.name, *args],
                              text=True, capture_output=True, check=False)


class InspectionTests(InspectionFixture, unittest.TestCase):

    def test_complete_section_preserves_exception_and_fenced_heading(self):
        result = self.run_helper("--heading", "^Retry$")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exception:", result.stdout)
        self.assertIn("not a section", result.stdout)
        self.assertNotIn("Unrelated.", result.stdout)
        self.assertIn("matches=1 emitted=1 omitted=0", result.stdout)

    def test_output_budget_never_cuts_a_section(self):
        result = self.run_helper("--heading", "Retry", "--max-chars", "20")
        self.assertIn("emitted=0 omitted=1", result.stdout)
        self.assertIn("OMITTED whole section:", result.stdout)
        self.assertNotIn("Check UNKNOWN", result.stdout)

    def test_invalid_regex_is_an_error(self):
        result = self.run_helper("--heading", "[")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid regex", result.stderr)

    def test_no_match_is_explicit(self):
        result = self.run_helper("--match", "does-not-exist")
        self.assertIn("matches=0 emitted=0", result.stdout)

    def test_overlapping_globs_do_not_repeat_sources(self):
        result = self.run_helper("--heading", "Retry", "--glob", "*.md",
                                 "--glob", "fixture.md")
        self.assertIn("files=1 matches=1", result.stdout)

    def test_invalid_budget_is_an_error(self):
        self.assertEqual(self.run_helper("--max-chars", "0").returncode, 2)


if __name__ == "__main__":
    unittest.main()
