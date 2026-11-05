"""Exercise discovery across stacks, hidden policy, Git ignores and bounded output."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "package/.agents/skills/project-exploration/scripts"
sys.path.insert(0, str(SCRIPTS))
from project_inventory import inventory
from unittest.mock import patch


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()

    def write(self, name, text="fixture"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_helper(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "discover_project.py"), str(self.root), *args],
                              capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def test_stacks_and_cross_client_guidance(self):
        names = {"AGENTS.md", "api/AGENTS.md", ".claude/rules/testing.md", ".cursor/rules/style.mdc",
                 ".agents/skills/review/SKILL.md", ".claude/skills/test/SKILL.md", "skills/shared/SKILL.md",
                 ".github/instructions/paths.instructions.md", ".github/PULL_REQUEST_TEMPLATE.md",
                 ".github/workflows/test.yml", "CODEOWNERS", "docs/architecture.rst", "pyproject.toml",
                 "web/package.json", "worker/go.mod", "engine/Cargo.toml"}
        for name in names:
            self.write(name)
        self.write("node_modules/dependency/AGENTS.md")
        self.write(".venv/AGENTS.md")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = self.run_helper("--scope", "api")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual({r["path"] for r in data["candidates"]}, names)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(data["mode"], "filesystem")
        self.assertGreater(data["excluded_entries"], 0)

    def test_git_ignored_guidance_is_not_claimed(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        self.write(".gitignore", "ignored/\n")
        self.write("ignored/AGENTS.md")
        self.write("AGENTS.md")
        data = json.loads(self.run_helper().stdout)
        self.assertEqual(data["mode"], "git-index")
        self.assertEqual([r["path"] for r in data["candidates"]], ["AGENTS.md"])
        self.assertIsNone(data["head"])

    def test_limits_and_counts(self):
        for name in ("AGENTS.md", "README.md", "CONTRIBUTING.md"):
            self.write(name)
        result = self.run_helper("--limit", "1", "--max-chars", "2500")
        data = json.loads(result.stdout)
        self.assertEqual(len(data["candidates"]), 1)
        self.assertEqual(data["omitted_candidates"], 2)
        self.assertLessEqual(len(result.stdout), 2501)
        self.assertTrue(json.loads(self.run_helper("--max-files", "1").stdout)["scan_limit_reached"])
        self.assertEqual(self.run_helper("--max-chars", "10").returncode, 1)

    def test_ignored_local_rules_at_root_and_scoped_owners(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        self.write(".gitignore", ".claude/\napi/.agents/\n.github/\n")
        self.write(".claude/rules/tenant.md", "paths: api/**")
        self.write("api/.agents/skills/local/SKILL.md")
        self.write(".github/copilot-instructions.md")
        self.write(".github/skills/workflow/SKILL.md")
        data = json.loads(self.run_helper("--scope", "api").stdout)
        self.assertEqual({r["path"] for r in data["candidates"]},
                         {".claude/rules/tenant.md", "api/.agents/skills/local/SKILL.md",
                          ".github/copilot-instructions.md", ".github/skills/workflow/SKILL.md"})

    def test_scope_escape_and_invalid_limits(self):
        for args in (("--scope", "../escape"), ("--scope", "/tmp"), ("--limit", "0")):
            self.assertEqual(self.run_helper(*args).returncode, 2)

    def test_symlinks_do_not_escape_or_get_read(self):
        target = Path(self.temp.name) / "outside.md"
        target.write_text("never read this content")
        (self.root / "AGENTS.md").symlink_to(target)
        (self.root / "linked").symlink_to(Path(self.temp.name), target_is_directory=True)
        data = json.loads(self.run_helper().stdout)
        self.assertEqual(data["candidates"], [])
        self.assertTrue(any("symlink" in warning for warning in data["warnings"]))
        self.assertNotIn("never read", json.dumps(data))

    def test_ancestor_guidance_not_unrelated_directories(self):
        (self.root.parent / "AGENTS.md").write_text("ancestor policy")
        data = json.loads(self.run_helper().stdout)
        self.assertIn(str(self.root.parent / "AGENTS.md"), data["ancestor_instructions"])

    def test_git_and_walk_errors_are_explicit(self):
        def bad_walk(root, **kwargs):
            kwargs["onerror"](PermissionError("fixture denied"))
            return iter(())
        with patch("project_inventory.git", side_effect=FileNotFoundError), patch(
                "project_inventory.os.walk", side_effect=bad_walk):
            data = inventory(self.root, 10)
        self.assertEqual(len(data["warnings"]), 2)
        self.assertIn("walk failed", data["warnings"][1])


if __name__ == "__main__":
    unittest.main()
