"""Quota handling must stop further paid sessions and signal incomplete execution."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import run


class RunnerTests(unittest.TestCase):
    def test_quota_stops_after_one_attempt_and_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            auth = root/'auth.json'
            auth.write_text('{}')
            out = root/'results'
            args = ['run.py','--out',str(out),'--auth',str(auth),'--cases','bug','security']
            with patch('sys.argv',args), patch('run.run',return_value={'execution_status':'blocked_account_limit'}) as worker:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as error: run.main()
            self.assertEqual(error.exception.code,2)
            self.assertEqual(worker.call_count,1)
            self.assertEqual(len(json.loads((out/'summary.json').read_text())),1)


if __name__ == '__main__':
    unittest.main()
