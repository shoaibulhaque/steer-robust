"""Explicit allowlists and generated native-client resources cannot drift or omit dependencies."""
from pathlib import Path
import shutil
import tempfile
import unittest
from package_contract import contents, mode
from validate_package import validate

SOURCE = Path(__file__).resolve().parents[1] / 'src'


class DistributionChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for dest, origin in contents(True).items():
            path = self.root/dest
            path.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(SOURCE/origin,path)
            path.chmod(mode(dest,True))

    def rejects(self, phrase):
        errors,_ = validate(self.root,distribution=True)
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_complete_native_clients(self):
        self.assertEqual(validate(self.root,distribution=True)[0],[])

    def test_unlisted_guide_is_not_implicitly_published(self):
        path = self.root/'Steer-robust/private.md'
        path.write_text('# Private\nRead when needed.\n')
        self.rejects('unexpected distribution file')

    def test_private_or_development_files_are_rejected(self):
        for name in ('.env','trace.jsonl','dev/check.py','evals/answers.json','__pycache__/data.pyc'):
            path = self.root/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('synthetic fixture')
            with self.subTest(name=name): self.rejects('unexpected distribution file')
            path.unlink()

    def test_client_reference_omission_is_rejected(self):
        (self.root/'.claude/skills/security-audit/references/findings.md').unlink()
        self.rejects('missing required resource')

    def test_client_drift_is_rejected(self):
        path = self.root/'.claude/skills/engineering-change/SKILL.md'
        path.write_text(path.read_text().replace('Before editing code','After editing code'))
        self.rejects('client copy differs')

    def test_instruction_bridge_is_required(self):
        (self.root/'CLAUDE.md').write_text('@missing.md\n')
        self.rejects('missing canonical AGENTS import')

    def test_executable_mode_is_preserved(self):
        path = self.root/'.agents/skills/statechart/scripts/check.py'
        path.chmod(0o644)
        self.rejects('incorrect file permissions')


if __name__ == '__main__':
    unittest.main()
