"""Distribution regression checks; no model calls, installs or third-party dependencies."""
import io
from pathlib import Path
import tempfile
import unittest
import zipfile

import build_package as kit


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.source = kit.ROOT
        self.original_files = kit.FILES
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for name in kit.FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((self.source / name).read_bytes())
        kit.ROOT = self.root

    def tearDown(self):
        kit.ROOT = self.source
        kit.FILES = self.original_files
        self.temporary.cleanup()

    def test_reproducible_complete_portable_archive(self):
        data = kit.archive()
        self.assertEqual(data, kit.archive())
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(set(archive.namelist()), {f"{kit.NAME}/{p}" for p in kit.FILES})
            self.assertIsNone(archive.testzip())
            for entry in archive.infolist():
                self.assertEqual(entry.external_attr >> 16, 0o100644)
            archive.extractall(self.root / "extracted")
        extracted = self.root / "extracted" / kit.NAME
        for name in kit.FILES:
            self.assertEqual((extracted / name).read_bytes(), (self.source / name).read_bytes())
        kit.ROOT = extracted
        kit.validate()

    def test_private_and_development_files_cannot_leak(self):
        baseline = kit.archive()
        for name in (".env", "raw-trace.jsonl", "dev/private.py", "research/private.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("private sentinel", encoding="utf-8")
        self.assertEqual(baseline, kit.archive())

    def test_missing_linked_resource_is_rejected(self):
        (self.root / "EVAL_PLAN.md").unlink()
        with self.assertRaises(ValueError):
            kit.archive()

    def test_wrong_skill_name_is_rejected(self):
        path = self.root / "skills/systematic-debugging/SKILL.md"
        path.write_text(path.read_text().replace("name: systematic-debugging", "name: another-skill"))
        with self.assertRaises(ValueError):
            kit.archive()

    def test_broken_link_is_rejected(self):
        path = self.root / "README.md"
        path.write_text(path.read_text() + "\n[Missing](not-shipped.md)\n")
        with self.assertRaises(ValueError):
            kit.archive()

    def test_symlinked_resource_is_rejected(self):
        path = self.root / "LICENSE"
        path.unlink()
        path.symlink_to(self.root / "README.md")
        with self.assertRaises(ValueError):
            kit.archive()

    def test_allowlisted_skill_reference_survives_installation(self):
        folder = self.root / "skills" / kit.SKILLS[0]
        reference = folder / "references" / "example.md"
        reference.parent.mkdir(exist_ok=True)
        reference.write_text("# A supporting resource\n")
        entry = folder / "SKILL.md"
        entry.write_text(entry.read_text() + "\nRead [the example](references/example.md) when needed.\n")
        relative = reference.relative_to(self.root).as_posix()
        kit.FILES = (*kit.FILES, relative)
        with zipfile.ZipFile(io.BytesIO(kit.archive())) as archive:
            self.assertEqual(archive.read(f"{kit.NAME}/{relative}"), reference.read_bytes())

    def test_unlisted_skill_resource_is_rejected(self):
        path = self.root / "skills" / kit.SKILLS[0] / "private.jsonl"
        path.write_text("private trace")
        with self.assertRaises(ValueError):
            kit.archive()

    def test_missing_supporting_reference_is_rejected(self):
        path = self.root / "skills/test-driven-development/references/writing-good-tests.md"
        path.unlink()
        with self.assertRaises(ValueError):
            kit.archive()

    def test_consolidated_architecture_skill_and_attribution_are_distributed(self):
        self.assertIn("architecture-engineering", kit.SKILLS)
        self.assertNotIn("repository-engineering", kit.SKILLS)
        self.assertNotIn("design-for-change", kit.SKILLS)
        with zipfile.ZipFile(io.BytesIO(kit.archive())) as archive:
            prefix = f"{kit.NAME}/skills/architecture-engineering/"
            self.assertIn(prefix + "SKILL.md", archive.namelist())
            self.assertIn(prefix + "references/change-locality.md", archive.namelist())
            self.assertIn(prefix + "references/integration-and-migration.md", archive.namelist())
            self.assertIn(prefix + "references/architecture-plan-casebook.md", archive.namelist())
            self.assertIn(prefix + "LICENSE.txt", archive.namelist())
            self.assertIn(prefix + "NOTICE.md", archive.namelist())
            self.assertIn(b"Copyright (c) 2026 Maze", archive.read(prefix + "LICENSE.txt"))
            skill = archive.read(prefix + "SKILL.md").decode("utf-8")
            self.assertIn("Greenfield", skill)
            self.assertIn("Brownfield", skill)

    def test_missing_architecture_casebook_is_rejected(self):
        (self.root / "skills/architecture-engineering/references/architecture-plan-casebook.md").unlink()
        with self.assertRaises(ValueError):
            kit.archive()

    def test_retired_architecture_skills_are_not_packaged(self):
        with zipfile.ZipFile(io.BytesIO(kit.archive())) as archive:
            self.assertFalse(any("/skills/repository-engineering/" in n or
                                 "/skills/design-for-change/" in n for n in archive.namelist()))

    def test_missing_consolidated_attribution_is_rejected(self):
        (self.root / "skills/architecture-engineering/NOTICE.md").unlink()
        with self.assertRaises(ValueError):
            kit.archive()

    def test_missing_imported_license_is_rejected(self):
        (self.root / "skills/security-engineering/LICENSE.txt").unlink()
        with self.assertRaises(ValueError):
            kit.archive()


if __name__ == "__main__":
    unittest.main()
