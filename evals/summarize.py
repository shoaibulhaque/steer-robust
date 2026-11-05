#!/usr/bin/env python3
"""Prepare a local review report; never publish benchmark results into the repository."""
import argparse
import json
from pathlib import Path
from fixtures import SOURCE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cohorts', nargs='+', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    output = args.out.resolve()
    if output.exists() or output.is_relative_to(SOURCE):
        parser.error('out must be fresh and outside this repository; publication requires separate review')
    rows = []
    for cohort in args.cohorts:
        path = cohort/'regraded.json'
        results = json.loads(path.read_text()) if path.exists() else [
            json.loads(p.read_text()) for p in sorted(cohort.glob('*/result.json'))]
        rows += [{**row,'cohort':cohort.name} for row in results]
    lines = ['# Local behavioral evaluation review', '',
             'Private preparation artifact; not automatically approved for publication.', '',
             '| Cohort / task | Enabled | Execution | Correct | Required reads | Model proof | Seconds | Input / cached / output tokens |',
             '|---|---|---|---|---|---|---|---|']
    for row in rows:
        usage = row.get('usage', [])
        counts = [sum(u.get(key,0) for u in usage) for key in ('input_tokens','cached_input_tokens','output_tokens')]
        lines.append(f"| {row['cohort']} / {row['case']} | {row['enabled']} | {row.get('execution_status','legacy')} | {row['correct']} | "
                     f"{row['adherence']} | {row.get('model_tool_evidence','n/a')} | {row['seconds']} | "
                     + (' / '.join(map(str,counts)) if usage else 'unavailable') + ' |')
    lines += ['', f'Completed records shown: {len(rows)}.',
              'Native token counts only; monetary cost is unavailable. CLI default model was not pinned.',
              'Read evidence is separate from semantic adherence. Qualitative review is same-agent, not independent.',
              'Small public Python fixtures and sequential runs do not establish statistical superiority or live Claude behavior.']
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text('\n'.join(lines)+'\n')
    print(output)


if __name__ == '__main__':
    main()
