"""Model receipts are distinct from success claims and zero-exit truncated searches."""
import tempfile
from pathlib import Path
import unittest
from model_evidence import grade


class ModelEvidenceTests(unittest.TestCase):
    def test_zero_exit_without_completion_is_not_model_proof(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for suffix in ('tla','cfg','mmd'): (root/f'Model.{suffix}').write_text('fixture')
            item = {'type':'command_execution','exit_code':0,'command':'java -cp tools.jar tlc2.TLC -dfid 6 Model',
                    'aggregated_output':'TLC2 Version 2.19\nStarting level 6\nFinished in 00s'}
            report = grade(root,[{'type':'item.completed','item':item}])
            self.assertFalse(report['model_completion_observed'])
            self.assertFalse(report['model_tool_evidence'])

    def test_echoed_receipt_is_not_execution(self):
        with tempfile.TemporaryDirectory() as d:
            item = {'type':'command_execution','exit_code':0,'command':'echo python check.py',
                    'aggregated_output':'{"status":"passed_bounded_model","trace_states":0}'}
            self.assertFalse(grade(Path(d),[{'type':'item.completed','item':item}])['model_completion_observed'])

    def test_real_checker_pair_with_artifacts_is_recognized(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for suffix in ('tla','cfg','mmd'): (root/f'Model.{suffix}').write_text('fixture')
            events = []
            for status, code, count in [('safety_counterexample',1,4),('passed_bounded_model',0,0)]:
                events.append({'type':'item.completed','item':{'type':'command_execution','exit_code':code,
                    'command':'python3 .agents/skills/statechart/scripts/check.py model.tla',
                    'aggregated_output':f'{{"status":"{status}","trace_states":{count}}}'}})
            self.assertTrue(grade(root,events)['model_tool_evidence'])


if __name__ == '__main__':
    unittest.main()
