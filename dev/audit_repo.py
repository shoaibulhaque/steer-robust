#!/usr/bin/env python3
"""Read-only inventory and bounded sensitive-pattern audit; never prints matching values."""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SENSITIVE = re.compile(rb'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]{20,}'
                       rb'|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|/home/[^ /]+/|/Users/[^ /]+/')


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def main():
    tracked = [p.decode() for p in git('ls-files','-z').split(b'\0') if p]
    inventory, problems = [], []
    for name in tracked:
        dest = name.replace('package/','src/',1) if name.startswith('package/') else name
        dest = dest.replace('tools/','dev/',1) if dest.startswith('tools/') else dest
        path = ROOT/dest
        state = 'relocated' if dest != name else 'retained'
        if not path.is_file(): problems.append(f'missing tracked resource: {name}')
        inventory.append({'tracked':name,'current':dest,'state':state})
    current = [p for p in ROOT.rglob('*') if p.is_file() and not {'.git','dist','__pycache__'}.intersection(p.parts)]
    for path in current:
        # The audit's own regex is a rule definition, not a leaked credential.
        if path == Path(__file__).resolve(): continue
        if SENSITIVE.search(path.read_bytes()): problems.append(f'sensitive-pattern candidate: {path.relative_to(ROOT)}')
    historical = set()
    for commit in git('rev-list','--all').decode().splitlines():
        tree = git('ls-tree','-r',commit).decode().splitlines()
        for line in tree:
            meta, name = line.split('\t',1)
            kind, sha = meta.split()[1:]
            if kind != 'blob' or sha in historical: continue
            historical.add(sha)
            if SENSITIVE.search(git('cat-file','blob',sha)):
                problems.append(f'historical sensitive-pattern candidate: {commit[:8]}:{name}')
    result = {'tracked_file_count':len(tracked),'inventory':inventory,'current_source_files':len(current),
              'historical_unique_blobs_scanned':len(historical),'problems':problems,
              'limit':'Defined credential/path patterns only; not a security or history-cleanliness guarantee'}
    print(json.dumps(result,indent=2))
    return bool(problems)


if __name__ == '__main__':
    raise SystemExit(main())
