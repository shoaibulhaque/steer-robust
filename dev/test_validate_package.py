#!/usr/bin/env python3
"""Mutation tests: structural regressions must be detected, not merely clean input accepted."""
from pathlib import Path
import tempfile
import unittest
from validate_package import markdown, validate
from package_contract import REQUIRED, SKILL_ROOT, SKILLS, GUIDES, EXECUTABLES


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in REQUIRED:
            self.write(name, "" if name.endswith(".py") else "# Resource\n")
        self.write("CLAUDE.md", "@AGENTS.md\n")
        for name in GUIDES:
            self.write(name, "# Guide\nRead when needed.\n## Safe reruns\nCheck twice.\n")
        for name in EXECUTABLES:
            (self.root / name).chmod(0o755)
        for name in SKILLS:
            self.write(f"{SKILL_ROOT}/{name}/SKILL.md", f"---\nname: {name}\ndescription: Scoped workflow.\n---\n")
        guides = "".join(f"[Guide]({name})\n" for name in sorted(GUIDES))
        links = "".join(f"[Skill]({SKILL_ROOT}/{name}/SKILL.md)\n" for name in SKILLS)
        self.write("AGENTS.md", "# Root\n[Guide](Steer-robust/efficiency.md#safe-reruns)\n" + links + guides)
        self.write("Steer-robust/efficiency.md", "# Guide\n\nRead when automating.\n\n## Safe reruns\nCheck twice.\n")

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
        self.assertEqual(set(stats), REQUIRED | {"Steer-robust/efficiency.md"})

    def test_missing_target(self):
        self.write("AGENTS.md", "[Gone](missing.md)\n[Guide](Steer-robust/efficiency.md)\n")
        self.rejects("missing target")

    def test_missing_anchor(self):
        self.write("AGENTS.md", "[Guide](Steer-robust/efficiency.md#nonexistent)\n")
        self.rejects("missing anchor")

    def test_orphan_guide(self):
        self.write("Steer-robust/orphan.md", "# Orphan\nRead when needed.\n")
        self.rejects("not directly linked")

    def test_missing_trigger(self):
        self.write("Steer-robust/efficiency.md", "# Guide\n## Safe reruns\n")
        self.rejects("missing Read when")

    def test_lines_are_not_a_quality_gate(self):
        self.write("README.md", "line\n" * 121)
        self.assertEqual(validate(self.root)[0], [])

    def test_entrypoint_word_budget(self):
        self.write("AGENTS.md", "[Guide](Steer-robust/efficiency.md)\n" + "word " * 451)
        self.rejects("exceeds 450")

    def test_guide_word_budget(self):
        self.write("Steer-robust/efficiency.md", "# Guide\nRead when needed.\n## Safe reruns\n" + "word " * 651)
        self.rejects("exceeds 650")

    def test_portability(self):
        for target in ("../outside.md", "/tmp/outside.md", "%2e%2e/outside.md", "file:///tmp/outside.md"):
            with self.subTest(target=target):
                self.write("AGENTS.md", f"[Bad]({target})\n[Guide](Steer-robust/efficiency.md)\n")
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
        self.write("AGENTS.md", (self.root / "AGENTS.md").read_text() +
                   "[Encoded](Steer-robust/%65fficiency.md#safe%2Dreruns)\n")
        self.assertEqual(validate(self.root)[0], [])


if __name__ == "__main__":
    unittest.main()
