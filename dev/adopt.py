#!/usr/bin/env python3
"""Install a project bundle only into absent/identical paths; never overwrite local policy."""
import argparse
from pathlib import Path
import shutil
from package_contract import contents, mode
from validate_package import validate

PACKAGE = Path(__file__).resolve().parents[1] / 'src'


def plan(target, client):
    manifest = contents(distribution=client in ('claude','both'))
    files = [(PACKAGE/origin, target/dest) for dest, origin in sorted(manifest.items())]
    conflicts = []
    for source, dest in files:
        if any(p.is_symlink() for p in (dest, *dest.parents) if p.is_relative_to(target)):
            conflicts.append(str(dest.relative_to(target)))
        elif dest.exists() and (not dest.is_file() or dest.read_bytes() != source.read_bytes()):
            conflicts.append(str(dest.relative_to(target)))
        elif any(p.exists() and not p.is_dir() for p in dest.parents if p.is_relative_to(target)):
            conflicts.append(str(dest.relative_to(target)))
    return files, sorted(set(conflicts))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('target', type=Path)
    p.add_argument('--client', choices=['codex', 'claude', 'both'], default='both')
    p.add_argument('--apply', action='store_true', help='copy only after an all-path conflict check')
    a = p.parse_args()
    target = a.target.absolute()
    errors, _ = validate(PACKAGE)
    if errors:
        p.exit(1, "Invalid canonical source; no files copied:\n" + "\n".join(errors) + "\n")
    files, conflicts = plan(target, a.client)
    if conflicts:
        p.exit(1, 'Manual merge required; no files changed:\n' + '\n'.join(conflicts) + '\n')
    missing = [(s, d) for s, d in files if not d.exists()]
    if a.apply:
        for source, dest in missing:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            dest.chmod(mode(dest.relative_to(target).as_posix(), a.client in ("claude", "both")))
    print(f"{'Copied' if a.apply else 'Would copy'} {len(missing)} files; {len(files)-len(missing)} identical")
    print('Verify native skill availability in a fresh session. Existing differing instructions require manual merge.')


if __name__ == '__main__':
    main()
