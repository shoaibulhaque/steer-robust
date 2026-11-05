"""Reject malformed metadata and missing/leaking distribution resources."""
from pathlib import Path
import shutil
import tempfile
import unittest
from package_contract import REQUIRED, SKILLS, SKILL_ROOT, SCRIPT_ROOT
from validate_package import validate

PACKAGE = Path(__file__).resolve().parents[1] / "src"


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "src"
        shutil.copytree(PACKAGE, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.skill = self.root / SKILL_ROOT / "change-verification/SKILL.md"
        self.script = self.root / SCRIPT_ROOT / "discover_project.py"

    def rejects(self, expected):
        errors, _ = validate(self.root)
        self.assertTrue(any(expected in item for item in errors), errors)

    def test_actual_distribution(self):
        self.assertEqual(validate(self.root)[0], [])

    def test_required_resources(self):
        for name in sorted(REQUIRED - {"AGENTS.md"}):
            path = self.root / name
            content = path.read_bytes()
            path.unlink()
            with self.subTest(name=name):
                self.rejects("missing required resource")
            path.write_bytes(content)

    def test_unexpected_data_not_shipped(self):
        (self.root / ".env").write_text("synthetic=fixture")
        self.rejects("unexpected distribution file")

    def test_invalid_python(self):
        self.script.write_text("def broken(:\n")
        self.rejects("invalid Python")

    def test_script_length_is_not_a_quality_gate(self):
        self.script.write_text("# line\n" * 121)
        self.assertEqual(validate(self.root)[0], [])

    def test_skill_metadata(self):
        for text, error in (("# No metadata", "frontmatter"),
                            ("---\nname: another\ndescription: Fine.\n---\n", "name must match"),
                            ("---\nname: change-verification\n---\n", "description must")):
            with self.subTest(error=error):
                self.skill.write_text(text)
                self.rejects(error)

    def test_unreadable_metadata(self):
        self.skill.write_bytes(b"\xff")
        self.rejects("unreadable metadata")

    def test_unfinished_skill(self):
        self.skill.write_text(self.skill.read_text() + "\nTODO\n")
        self.rejects("unfinished scaffold")

    def test_skill_word_budget(self):
        self.skill.write_text(self.skill.read_text() + " word" * 451)
        self.rejects("words exceeds 450")

    def test_missing_root_skill_link(self):
        root = self.root / "AGENTS.md"
        original = root.read_text()
        for skill in SKILLS:
            with self.subTest(skill=skill):
                root.write_text(original.replace(f"{SKILL_ROOT}/{skill}/SKILL.md", "README.md"))
                self.rejects(f"{skill}: not directly linked")
        root.write_text(original)

    def test_cache_not_archived(self):
        cache = self.root / SCRIPT_ROOT / "__pycache__/ignore.pyc"
        cache.parent.mkdir()
        cache.write_bytes(b"cache")
        errors, stats = validate(self.root)
        self.assertTrue(any("unexpected distribution file" in error for error in errors))
        self.assertFalse(any(name.endswith(".pyc") for name in stats))

    def test_symlink_resource(self):
        self.script.unlink()
        self.script.symlink_to(self.root / SCRIPT_ROOT / "project_inventory.py")
        self.rejects("symlink resources")


if __name__ == "__main__":
    unittest.main()
