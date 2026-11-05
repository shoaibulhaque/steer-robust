"""Reapply versioned independent graders to retained trials without rerunning or relabeling workers."""
import argparse
import json
from pathlib import Path
from outcomes import grade as outcome
from regression import grade as regression
from traces import grade as process, execution_status
from model_evidence import grade as model_evidence


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('run', type=Path)
    a = p.parse_args()
    rows = []
    for result in sorted(a.run.glob('*/result.json')):
        old = json.loads(result.read_text())
        trial, root = result.parent, result.parent / 'repo'
        events = [json.loads(line) for line in (trial/'events.jsonl').read_text().splitlines() if line.strip()]
        row = {**old, **outcome(old['case'], root), **regression(old['case'], root),
               **process(old['case'], root, events, (trial/'prompt.json').read_text(), old['enabled'])}
        if row['case'] == 'stateful':
            row.update(model_evidence(root, events))
        row['execution_status'] = execution_status(events, row['exit'])
        row['successful_behavior'] = bool(row['exit'] == 0 and row['correct'] and (row['discriminating_tests'] or row['case'] in ('security','testvalue','honesty'))
                                          and not row['guidance_changed'] and row.get('model_tool_evidence', True))
        rows.append(row)
    (a.run/'regraded.json').write_text(json.dumps(rows, indent=2)+'\n')
    for row in rows:
        print(row['case'], row['enabled'], 'correct=', row['correct'], 'regression=',
              row['discriminating_tests'], 'read adherence=', row['adherence'])


if __name__ == '__main__':
    main()
