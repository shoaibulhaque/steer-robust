#!/usr/bin/env python3
"""List candidate project guidance, not a complete policy or an execution plan."""
import argparse
import json
import os
from itertools import islice
from pathlib import Path
from project_inventory import AGENT_NAMES, EXCLUDED, inventory


def guidance_extras(root, scopes):
    """Probe known local guidance even when Git ignores it; never inspect dependency trees."""
    owners = {Path(".")}
    for scope in scopes:
        owners.update(scope.parents)
        owners.add(scope if (root / scope).is_dir() else scope.parent)
    def fail(error):
        raise error
    for owner in sorted(owners):
        base = root / owner
        for name in ("AGENTS.md", "AGENTS.override.md", "CLAUDE.md", "GEMINI.md", ".cursorrules",
                     ".github/copilot-instructions.md"):
            if (base / name).is_file() or (base / name).is_symlink():
                yield (owner / name).as_posix()
        for folder in (".agents", ".claude", ".cursor", ".github/instructions", ".github/skills"):
            location = base / folder
            if location.is_symlink():
                yield location.relative_to(root).as_posix()
                continue
            if not location.exists():
                continue
            for directory, dirs, files in os.walk(location, followlinks=False, onerror=fail):
                dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(directory) / d).is_symlink())
                for name in sorted(files):
                    yield (Path(directory) / name).relative_to(root).as_posix()


def discover(root, scopes, maximum=50000):
    extras = list(islice(guidance_extras(root, scopes), maximum + 1))
    result = inventory(root, maximum, extras)
    ancestors = [str(parent / name) for parent in root.parents
                 for name in ("AGENTS.md", "AGENTS.override.md", "CLAUDE.md")
                 if (parent / name).is_file() or (parent / name).is_symlink()]

    def priority(record):
        path = Path(record["path"])
        owner = path.parent
        related = any(owner == s or owner in s.parents or s in owner.parents for s in scopes)
        is_global = len(path.parts) == 1 or path.parts[0].startswith(".")
        rank = 0 if path.name.lower() in AGENT_NAMES and (related or is_global) else 1
        rank += 0 if related or is_global or not scopes else 2
        kind_rank = {"instructions": 0, "conditional-rule": 1, "skill": 2,
                     "documentation": 3, "ownership": 4, "toolchain": 5, "ci": 6, "template": 7}
        return rank, kind_rank[record["kind"]], len(path.parts), record["path"]

    result["candidates"].sort(key=priority)
    result.update(root=str(root), scope_priority=[s.as_posix() for s in scopes],
                  ancestor_instructions=ancestors, excluded_directory_names=sorted(EXCLUDED),
                  identity_note="HEAD is not a snapshot of uncommitted working files",
                  extra_guidance_scan="Root and explicit scope ancestors, including ignored agent folders",
                  coverage="Filename heuristics only; inspect conditions and follow relevant links")
    return result


def bounded(result, limit, budget):
    candidates, warnings = result.pop("candidates"), result.pop("warnings")
    result.update(candidates_found=len(candidates), candidates=[], warnings=warnings[:8],
                  omitted_candidates=len(candidates), omitted_warnings=max(0, len(warnings) - 8))
    for record in candidates[:limit]:
        result["candidates"].append(record)
        result["omitted_candidates"] -= 1
        if len(json.dumps(result, ensure_ascii=True, indent=2)) > budget:
            result["candidates"].pop()
            result["omitted_candidates"] += 1
            break
    rendered = json.dumps(result, ensure_ascii=True, indent=2)
    if len(rendered) > budget:
        raise ValueError("metadata exceeds max-chars; raise the budget to retain coverage warnings")
    return rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--scope", action="append", default=[], help="relative affected path; prioritizes, not filters")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--max-files", type=int, default=50000)
    parser.add_argument("--max-chars", type=int, default=12000)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir() or min(args.limit, args.max_files, args.max_chars) < 1:
        parser.error("root must be a directory; all limits must be positive")
    scopes = []
    for raw in args.scope:
        scope = (root / raw).resolve()
        if Path(raw).is_absolute() or not scope.is_relative_to(root):
            parser.error("scope must remain inside root")
        scopes.append(scope.relative_to(root))
    try:
        print(bounded(discover(root, scopes, args.max_files), args.limit, args.max_chars))
    except (OSError, ValueError) as error:
        parser.exit(1, f"discovery failed: {error}\n")


if __name__ == "__main__":
    main()
