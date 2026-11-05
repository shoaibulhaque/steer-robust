"""Integration: complete hidden resources survive packaging and execute after extraction."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile
from package_contract import SCRIPT_ROOT, REQUIRED, contents, mode

SOURCE = Path(__file__).resolve().parents[1]


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(SOURCE / "src", self.root / "src",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (self.root / "dev").mkdir()
        for name in ("build_package.py", "validate_package.py", "package_contract.py"):
            shutil.copy2(SOURCE / "dev" / name, self.root / "dev" / name)

    def build(self):
        return subprocess.run([sys.executable, str(self.root / "dev/build_package.py")],
                              capture_output=True, text=True,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=45)

    def test_archive_is_complete_executable_and_repeatable(self):
        first = self.build()
        self.assertEqual(first.returncode, 0, first.stderr)
        output = self.root / "dist/Steer-robust.zip"
        original = output.read_bytes()
        with ZipFile(output) as archive:
            self.assertIn(f"{SCRIPT_ROOT}/discover_project.py", archive.namelist())
            self.assertIn(".agents/skills/change-verification/SKILL.md", archive.namelist())
            for name in ("SKILL.md", "references/scenarios.md", "references/evidence.md"):
                self.assertIn(f".agents/skills/runtime-qa/{name}", archive.namelist())
            self.assertEqual(set(archive.namelist()), set(contents(True)))
            for name in archive.namelist():
                self.assertEqual(archive.getinfo(name).external_attr >> 16 & 0o777, mode(name, True))
            for skill in ("engineering-change", "security-audit", "statechart"):
                canonical = f".agents/skills/{skill}/SKILL.md"
                self.assertEqual(archive.read(canonical), archive.read(canonical.replace('.agents/', '.claude/')))
            self.assertFalse(any("research/" in p or "__pycache__" in p for p in archive.namelist()))
        second = self.build()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(original, output.read_bytes())

    def test_broken_distribution_is_rejected_before_archive(self):
        (self.root / "src" / SCRIPT_ROOT / "guidance_sections.py").unlink()
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required resource", result.stderr)
        self.assertFalse((self.root / "dist/Steer-robust.zip").exists())


if __name__ == "__main__":
    unittest.main()
