#!/usr/bin/env python3
"""Opt-in real Codex CLI paired trials; never invoked by ordinary CI."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from cases import CASES
from fixtures import SOURCE, create, environment
from outcomes import grade as outcome
from regression import grade as regression
from traces import grade as process, execution_status
from model_evidence import grade as model_evidence
from isolation import command as isolated, verify as verify_isolation


def run(a, case, enabled):
    label = f"{case}-{'enabled' if enabled else 'disabled'}"
    out = a.out / label
    out.mkdir(parents=True)
    root = out / 'repo'
    create(root, case, enabled)
    env = environment(out / 'runtime', a.auth.resolve())
    verify_isolation(out, env)
    prompt = CASES[case]['prompt'] + '\nUse standard-library unittest tests. Do not use subagents, network, installs, commits or publication.'
    (out / 'task.txt').write_text(prompt)
    snapshot = subprocess.run(isolated(['codex', 'debug', 'prompt-input', prompt], out, env), cwd=root, env=env,
                              text=True, capture_output=True, check=True, timeout=30).stdout
    (out / 'prompt.json').write_text(snapshot)
    cmd = ['codex', 'exec', '--ignore-user-config', '--ephemeral', '--json', '--sandbox',
           'workspace-write', '--skip-git-repo-check', '-C', str(root)]
    if a.model:
        cmd += ['--model', a.model]
    cmd.append(prompt)
    before = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
    (out / 'source-before.json').write_text(json.dumps(before, indent=2))
    start = time.monotonic()
    with (out / 'events.jsonl').open('w') as trace, (out / 'stderr.txt').open('w') as stderr:
        try:
            code = subprocess.run(isolated(cmd, out, env), stdin=subprocess.DEVNULL, stdout=trace, stderr=stderr,
                                  env=env, timeout=a.timeout).returncode
        except subprocess.TimeoutExpired:
            code = 124
    events = []
    for line in (out / 'events.jsonl').read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    after = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    result = {'case': case, 'enabled': enabled, 'grader_boundary': 'OS mount isolation verified', 'exit': code, 'seconds': round(time.monotonic()-start, 2),
              'model': a.model or 'CLI default (not overridden)',
              'cli_version': subprocess.check_output(['codex','--version'], text=True).strip(), 'changed_files': changed,
              'usage': [e['usage'] for e in events if e.get('type') == 'turn.completed'],
              **outcome(case, root), **regression(case, root),
              **process(case, root, events, snapshot, enabled)}
    if case == 'stateful':
        result.update(model_evidence(root, events))
    result['execution_status'] = execution_status(events, code)
    result['guidance_changed'] = any(k.startswith(('.agents/', 'Steer-robust/')) or k == 'AGENTS.md' for k in changed)
    result['successful_behavior'] = bool(code == 0 and result['correct'] and (result['discriminating_tests'] or case in ('security','testvalue','honesty'))
                                         and not result['guidance_changed'] and result.get('model_tool_evidence', True))
    (out / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--auth', type=Path, default=Path.home()/'.codex/auth.json')
    p.add_argument('--model', help='optional exact installed model; same for both arms')
    p.add_argument('--cases', nargs='+', choices=list(CASES), default=list(CASES))
    p.add_argument('--arm', choices=['both', 'enabled', 'disabled'], default='both')
    p.add_argument('--timeout', type=int, default=240)
    a = p.parse_args()
    a.out = a.out.resolve()
    if a.out.exists() or a.out.is_relative_to(SOURCE) or not a.auth.is_file():
        p.error('out must be fresh, outside the source repository; file auth must exist')
    a.out.mkdir(parents=True)
    results = []
    stop = False
    for index, case in enumerate(a.cases):
        # Alternate arm order to expose, rather than systematically favor, warm-run effects.
        arms = ([False, True] if index % 2 == 0 else [True, False]) if a.arm == 'both' else [a.arm == 'enabled']
        for enabled in arms:
            result = run(a, case, enabled)
            results.append(result)
            if result['execution_status'] in ('blocked_account_limit', 'blocked_executor'):
                print('Stopped: resolve the external execution blocker before retrying.', flush=True)
                stop = True
                break
        if stop:
            break
    (a.out/'summary.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
