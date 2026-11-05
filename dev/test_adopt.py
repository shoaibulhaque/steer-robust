"""Client layout, conflict safety and repeatability, without running a model."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from adopt import PACKAGE


class AdoptionTests(unittest.TestCase):
    def test_both_clients_and_safe_rerun(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / 'repo'
            command = [sys.executable, str(Path(__file__).with_name('adopt.py')), str(target)]
            subprocess.run(command, check=True, capture_output=True)
            self.assertFalse(target.exists())
            subprocess.run([*command, '--apply'], check=True, capture_output=True)
            for skill in (PACKAGE / '.agents/skills').iterdir():
                if not skill.is_dir(): continue
                a, b = target / '.agents/skills' / skill.name, target / '.claude/skills' / skill.name
                self.assertEqual((a / 'SKILL.md').read_bytes(), (b / 'SKILL.md').read_bytes())
                self.assertTrue((b / '../../../Steer-robust/design.md').resolve().exists())
            snapshot = {str(p): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            subprocess.run([*command, '--apply'], check=True, capture_output=True)
            self.assertEqual(snapshot, {str(p): p.read_bytes() for p in target.rglob('*') if p.is_file()})

    def test_conflict_causes_no_partial_copy(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)
            (target / 'AGENTS.md').write_text('project-owned')
            r = subprocess.run([sys.executable, str(Path(__file__).with_name('adopt.py')), d, '--apply'],
                               capture_output=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertEqual([p.name for p in target.iterdir()], ['AGENTS.md'])

    def test_symlink_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            target, outside = Path(d) / 'repo', Path(d) / 'outside'
            target.mkdir(); outside.mkdir()
            (target / '.agents').symlink_to(outside, target_is_directory=True)
            r = subprocess.run([sys.executable, str(Path(__file__).with_name('adopt.py')), str(target), '--apply'],
                               capture_output=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
