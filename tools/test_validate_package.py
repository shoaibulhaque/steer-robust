#!/usr/bin/env python3
"""Mutation tests: structural regressions must be detected, not merely clean input accepted."""
from pathlib import Path
import tempfile
import unittest
from validate_package import markdown, validate
from package_contract import REQUIRED, SKILL_ROOT, SKILLS


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in REQUIRED:
            self.write(name, "" if name.endswith(".py") else "# Resource\n")
        for name in SKILLS:
            self.write(f"{SKILL_ROOT}/{name}/SKILL.md", f"---\nname: {name}\ndescription: Scoped workflow.\n---\n")
        links = "".join(f"[Skill]({SKILL_ROOT}/{name}/SKILL.md)\n" for name in SKILLS)
        self.write("AGENTS.md", "# Root\n[Guide](Steer-robust/guide.md#safe-reruns)\n" + links)
        self.write("Steer-robust/guide.md", "# Guide\n\nRead when automating.\n\n## Safe reruns\nCheck twice.\n")

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def rejects(self, text):
        errors, _ = validate(self.root)
        self.assertTrue(any(text in error for error in errors), errors)

    def test_valid_package(self):
        errors, stats = validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(set(stats), REQUIRED | {"Steer-robust/guide.md"})

    def test_missing_target(self):
        self.write("AGENTS.md", "[Gone](missing.md)\n[Guide](Steer-robust/guide.md)\n")
        self.rejects("missing target")

    def test_missing_anchor(self):
        self.write("AGENTS.md", "[Guide](Steer-robust/guide.md#nonexistent)\n")
        self.rejects("missing anchor")

    def test_orphan_guide(self):
        self.write("Steer-robust/orphan.md", "# Orphan\nRead when needed.\n")
        self.rejects("not directly linked")

    def test_missing_trigger(self):
        self.write("Steer-robust/guide.md", "# Guide\n## Safe reruns\n")
        self.rejects("missing Read when")

    def test_line_budget(self):
        self.write("README.md", "line\n" * 121)
        self.rejects("exceeds 120")

    def test_entrypoint_word_budget(self):
        self.write("AGENTS.md", "[Guide](Steer-robust/guide.md)\n" + "word " * 451)
        self.rejects("exceeds 450")

    def test_guide_word_budget(self):
        self.write("Steer-robust/guide.md", "# Guide\nRead when needed.\n## Safe reruns\n" + "word " * 651)
        self.rejects("exceeds 650")

    def test_portability(self):
        for target in ("../outside.md", "/tmp/outside.md", "%2e%2e/outside.md", "file:///tmp/outside.md"):
            with self.subTest(target=target):
                self.write("AGENTS.md", f"[Bad]({target})\n[Guide](Steer-robust/guide.md)\n")
                self.rejects("non-portable")

    def test_symlink_escape(self):
        (self.root / "escape.md").symlink_to(self.root.parent / "outside.md")
        self.rejects("file escapes")

    def test_fences_and_repeated_headings(self):
        text = "# A\n## Same!\n## Same!\n```md\n[Fake](missing.md)\n# Fake\n```example\n# Hidden\n```\n"
        links, anchors = markdown(text)
        self.assertEqual(links, [])
        self.assertEqual(anchors, {"a", "same", "same-1"})

    def test_empty_package(self):
        (self.root / "AGENTS.md").unlink()
        self.rejects("missing AGENTS.md")

    def test_encoded_path_and_fragment(self):
        self.write("Steer-robust/two words.md", "# Two\nRead when needed.\n## Safe reruns\n")
        self.write("AGENTS.md", (self.root / "AGENTS.md").read_text() +
                   "[Two](Steer-robust/two%20words.md#safe%2Dreruns)\n")
        self.assertEqual(validate(self.root)[0], [])


if __name__ == "__main__":
    unittest.main()
