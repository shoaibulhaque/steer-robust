"""Parser and subprocess behavior, with no optional dependencies required in CI."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'src/.agents/skills/statechart/scripts/check.py'
spec = importlib.util.spec_from_file_location('statechart_check', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
TRACE = 'Error: Invariant Safe is violated.\nState 1: <Initial predicate>\n/\\ phase = "open"\n\nState 2: <Close>\n/\\ phase = "closed"\n\n'


class StatechartTests(unittest.TestCase):
    def invoke(self, text, code=0, timeout=False):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for name in ('Model.tla', 'Model.cfg', 'tlc.jar'):
            (root / name).write_text('fixture')
        fake = root / 'java'
        fake.write_text('#!/usr/bin/env python3\n' + ('import time; time.sleep(5)\n' if timeout else
                        f'print({text!r})\nraise SystemExit({code})\n'))
        fake.chmod(0o755)
        r = subprocess.run([sys.executable, str(SCRIPT), str(root / 'Model.tla'), '--config',
                            str(root / 'Model.cfg'), '--jar', str(root / 'tlc.jar'), '--java', str(fake),
                            '--timeout', '1', '--out', str(root / 'out')], capture_output=True)
        return r, root / 'out'

    def test_safety_path_and_mermaid_escaping(self):
        trace = checker.states(TRACE)
        self.assertEqual(len(trace), 2)
        chart = checker.mermaid(trace)
        self.assertIn('S1 --> S2', chart)
        self.assertNotIn('"closed"', chart)
        result, out = self.invoke(TRACE, 12)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads((out / 'report.json').read_text())['status'], 'safety_counterexample')
        self.assertTrue((out / 'trace.mmd').exists())

    def test_unrecognized_success_fails_closed(self):
        result, out = self.invoke('everything fine')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads((out / 'report.json').read_text())['status'], 'tool_error')

    def test_success_requires_completion(self):
        result, out = self.invoke('Model checking completed. No error has been found.')
        self.assertEqual(result.returncode, 0)
        self.assertFalse((out / 'trace.mmd').exists())

    def test_depth_limited_zero_exit_is_not_success(self):
        result, out = self.invoke('Running depth-first search Model-Checking\nStarting level 1024\nFinished in 00s')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads((out / 'report.json').read_text())['status'], 'tool_error')

    def test_timeout_is_not_a_pass(self):
        result, out = self.invoke('', timeout=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads((out / 'report.json').read_text())['status'], 'timeout')

    def test_unparsed_trace_is_not_a_chart(self):
        result, out = self.invoke('Error: Invariant Safe is violated.', 12)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads((out / 'report.json').read_text())['status'], 'unparsed_counterexample')
        self.assertFalse((out / 'trace.mmd').exists())


if __name__ == '__main__':
    unittest.main()
