"""Evidence grader: actual completed tool reads, native discovery snapshot and tool actions."""
import json
from pathlib import Path
import re
import shlex
import fnmatch
from cases import CASES


def completed(events):
    return [e['item'] for e in events if e.get('type') == 'item.completed' and 'item' in e]


def reader_command(command, path):
    try:
        outer = shlex.split(command)
        if outer and Path(outer[0]).name in ('sh','bash','zsh') and any(x in outer for x in ('-c','-lc')):
            command = outer[-1]
        lexer = shlex.shlex(command, posix=True, punctuation_chars=';&|')
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return False
    segments, current = [], []
    for token in tokens + [';']:
        if token in (';', '&&', '||', '|'):
            if current: segments.append(current)
            current = []
        else:
            current.append(token)
    for segment in segments:
        if Path(segment[0]).name not in ('cat','sed','head','tail'):
            continue
        for token in segment[1:]:
            if token.startswith('-'): continue
            brace = re.fullmatch(r'([^{}]*)\{([^{}]+)\}([^{}]*)', token)
            variants = [brace[1]+part+brace[3] for part in brace[2].split(',')] if brace else [token]
            if any(value == str(path) or str(path).endswith('/' + value)
                   or fnmatch.fnmatch(str(path), '*/' + value) for value in variants):
                return True
    return False


def loaded(path, items):
    # A full source body and a real successful reader invocation are both necessary.
    body = path.read_text().strip()
    return any(item.get('type') == 'command_execution' and item.get('exit_code') == 0
               and body and body in item.get('aggregated_output', '')
               and reader_command(item.get('command',''), path) for item in items)


def advertised(path, snapshot):
    # Native Codex compresses paths using the documented skill-roots table.
    data = json.loads(snapshot)
    text = '\n'.join(c.get('text', '') for item in data for c in item.get('content', [])
                     if isinstance(c, dict))
    roots = dict(re.findall(r"^- `(r\d+)` = `([^`]+)`$", text, re.M))
    entries = re.findall(r"^- [^\n]+ \(file: (r\d+)/([^\n]+)\)$", text, re.M)
    return any((Path(roots[alias]) / suffix).resolve() == path.resolve()
               for alias, suffix in entries if alias in roots)


def grade(case, root, events, prompt_snapshot, enabled):
    items = completed(events)
    skills, guides = {}, {}
    for name in CASES[case]['skills']:
        path = root / '.agents/skills' / name / 'SKILL.md'
        skills[name] = {'advertised': advertised(path, prompt_snapshot),
                        'loaded': loaded(path, items) if enabled and path.is_file() else False}
    for name in CASES[case]['guides']:
        path = root / 'Steer-robust' / f'{name}.md'
        guides[name] = loaded(path, items) if enabled and path.is_file() else False
    references = {}
    required_refs = {'stateful': ['statechart/references/model-checking.md'],
                     'security': ['security-audit/references/findings.md', 'security-audit/references/access.md',
                                  'security-audit/references/inputs.md']}.get(case, [])
    for name in required_refs:
        path = root / '.agents/skills' / name
        references[name] = loaded(path, items) if enabled and path.exists() else False
    all_skills = {p.parent.name: loaded(p, items) for p in (root/'.agents/skills').glob('*/SKILL.md')} if enabled else {}
    all_guides = {p.stem: loaded(p, items) for p in (root/'Steer-robust').glob('*.md')} if enabled else {}
    commands = [i for i in items if i.get('type') == 'command_execution']
    tests = [i for i in commands if re.search(r'python[\d.]* .*?(unittest|test_|assert |ledger.py)', i.get('command', ''), re.S)]
    # Test execution is an observable action only; outcomes.py and regression grading decide correctness.
    return {'skills': skills, 'guides': guides, 'tool_calls': len(commands),
            'failed_tool_calls': sum(i.get('exit_code') != 0 for i in commands),
            'test_commands_observed': len(tests),
            'references': references,
            'additional_skills_loaded': [k for k,v in all_skills.items() if v and k not in skills],
            'additional_guides_loaded': [k for k,v in all_guides.items() if v and k not in guides],
            'adherence': bool(enabled and all(v['advertised'] and v['loaded'] for v in skills.values())
                              and all(guides.values()) and all(references.values()))}


def execution_status(events, code):
    failures = [e for e in events if e.get('type') in ('error','turn.failed')]
    if any('usage limit' in json.dumps(e).lower() for e in failures):
        return 'blocked_account_limit'
    commands = [e['item'] for e in events if e.get('type')=='item.completed'
                and e.get('item',{}).get('type')=='command_execution']
    if commands and all(item.get('exit_code') == -1 for item in commands):
        return 'blocked_executor'
    return 'completed' if code == 0 and any(e.get('type')=='turn.completed' for e in events) else 'incomplete_execution'
