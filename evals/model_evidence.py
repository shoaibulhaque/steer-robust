"""Check actual model-checker receipts separately from implementation correctness."""
import json
from pathlib import Path
import shlex


def grade(root, events):
    broken, passed, attempts = False, False, 0
    for event in events:
        item = event.get('item', {})
        if event.get('type') != 'item.completed' or item.get('type') != 'command_execution': continue
        command, output = item.get('command',''), item.get('aggregated_output','')
        try:
            words = shlex.split(command)
            if words and Path(words[0]).name in ('sh','bash','zsh'):
                words = shlex.split(words[-1])
            # Ignore explicit environment assignments; never accept echo/agent-message claims.
            while words and '=' in words[0] and not words[0].startswith('/'):
                words.pop(0)
        except ValueError:
            continue
        wrapper = len(words)>1 and Path(words[0]).name.startswith('python') and Path(words[1]).name == 'check.py'
        direct = words and Path(words[0]).name == 'java' and 'tlc2.TLC' in words
        if wrapper:
            for line in output.splitlines():
                try: receipt = json.loads(line)
                except json.JSONDecodeError: continue
                if not isinstance(receipt,dict) or 'trace_states' not in receipt: continue
                attempts += 1
                broken |= receipt.get('status') == 'safety_counterexample' and receipt['trace_states'] > 0
                passed |= receipt.get('status') == 'passed_bounded_model' and item.get('exit_code') == 0
        elif direct and output.startswith('TLC2 Version'):
            attempts += 1
            broken |= ' is violated' in output and 'State 1:' in output and item.get('exit_code') != 0
            passed |= 'Model checking completed. No error has been found.' in output and item.get('exit_code') == 0
    artifacts = all(any(root.rglob(pattern)) for pattern in ('*.tla','*.cfg','*.mmd'))
    return {'model_tool_evidence': bool(broken and passed and artifacts),
            'model_counterexample_observed': broken, 'model_completion_observed': passed,
            'model_attempts': attempts, 'model_artifacts_present': artifacts}
