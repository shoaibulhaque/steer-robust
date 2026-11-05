"""Check preservation of scope context and explicit retrieval failures."""
import unittest
from test_inspect_guidance import InspectionFixture


class ContextTests(InspectionFixture, unittest.TestCase):
    def write(self, text):
        from pathlib import Path
        path = Path(self.directory.name) / "fixture.md"
        path.write_text(text)
        return path

    def test_nested_scope_and_children_survive(self):
        self.write("---\npaths: api/**\n---\n# Rules\nOnly for writes.\n## Retry\nUse bounded retries.\n"
                   "### Exception\nUnknown effects require reconciliation.\n## Other\nUnrelated.\n")
        result = self.run_helper("--heading", "^Retry$")
        self.assertEqual(result.returncode, 0, result.stderr)
        for phrase in ("paths: api/**", "Only for writes", "### Exception", "require reconciliation"):
            self.assertIn(phrase, result.stdout)
        self.assertNotIn("Unrelated", result.stdout)

    def test_match_does_not_pull_entire_parent(self):
        self.write("# Root\nParent context.\n## Useful\nNeedle.\n## Other\nUnrelated.\n")
        result = self.run_helper("--match", "Needle")
        self.assertIn("Parent context", result.stdout)
        self.assertIn("Needle", result.stdout)
        self.assertNotIn("Unrelated", result.stdout)

    def test_overlapping_selected_sections_are_not_repeated(self):
        self.write("# Root\nOverview.\n## Parent\nBody.\n### Child\nChild body.\n")
        result = self.run_helper("--heading", "Parent|Child")
        self.assertEqual(result.stdout.count("Child body."), 1)
        self.assertIn("matches=1 emitted=1", result.stdout)

    def test_escape_globs_are_errors(self):
        self.assertEqual(self.run_helper("--glob", "../*.md").returncode, 2)
        self.assertEqual(self.run_helper("--glob", "/tmp/*.md").returncode, 2)

    def test_symlink_is_explicitly_skipped(self):
        path = self.write("source body")
        alias = path.with_name("alias.md")
        alias.symlink_to(path)
        result = self.run_helper("--glob", "alias.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("SKIPPED", result.stdout)
        self.assertNotIn("source body", result.stdout)

    def test_large_or_invalid_file_is_not_silently_accepted(self):
        path = self.write("# Long\n" + "x" * 100)
        result = self.run_helper("--max-file-bytes", "20")
        self.assertEqual(result.returncode, 1)
        self.assertIn("max-file-bytes", result.stdout)
        path.write_bytes(b"\xff")
        self.assertEqual(self.run_helper().returncode, 1)

    def test_file_limit_reports_unscanned_sources(self):
        path = self.write("# One\n")
        path.with_name("two.md").write_text("# Two\n")
        self.assertIn("unscanned_files=1", self.run_helper("--max-files", "1").stdout)

    def test_shared_context_is_emitted_once(self):
        self.write("# Root\nTenant-only context.\n## One\nFirst.\n## Two\nSecond.\n")
        result = self.run_helper("--heading", "One|Two")
        self.assertEqual(result.stdout.count("Tenant-only context."), 1)
        self.assertIn("First.", result.stdout)
        self.assertIn("Second.", result.stdout)

    def test_omitted_first_selection_does_not_lose_context(self):
        self.write("# Root\nScope: writes.\n## Large\n" + "x" * 5000 + "\n## Small\nSafe.\n")
        result = self.run_helper("--heading", "Large|Small", "--max-chars", "250")
        self.assertIn("Scope: writes.", result.stdout)
        self.assertIn("Safe.", result.stdout)
        self.assertIn("emitted=1 omitted=1", result.stdout)


if __name__ == "__main__":
    unittest.main()
