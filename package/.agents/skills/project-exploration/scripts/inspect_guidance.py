#!/usr/bin/env python3
"""Index Markdown or select complete sections with scope context; no interpretation."""
import argparse
from pathlib import Path
import re
from guidance_sections import headings, selections


def pattern(value, parser):
    try:
        return re.compile(value, re.I) if value else None
    except re.error as error:
        parser.error(f"invalid regex: {error}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--glob", action="append", dest="globs")
    parser.add_argument("--heading", help="regex over section headings")
    parser.add_argument("--match", help="regex over directly owned section text")
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--max-file-bytes", type=int, default=1048576)
    parser.add_argument("--max-files", type=int, default=200)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir() or min(args.max_chars, args.max_file_bytes, args.max_files) < 1:
        parser.error("root must be a directory and limits must be positive")
    heading, match = pattern(args.heading, parser), pattern(args.match, parser)
    paths = set()
    for glob in args.globs or ["*.md"]:
        if Path(glob).is_absolute() or ".." in Path(glob).parts:
            parser.error("globs must remain inside root")
        try:
            paths.update(p for p in root.glob(glob) if p.is_file())
        except (ValueError, OSError) as error:
            parser.error(f"glob failed: {error}")
    outputs, problems, total = [], [], 0
    for path in sorted(paths)[:args.max_files]:
        name = path.relative_to(root).as_posix()
        try:
            if not path.resolve().is_relative_to(root) or any(
                    p.is_symlink() for p in (path, *path.parents) if p != root and p.is_relative_to(root)):
                raise ValueError("symlink/escaping source; inspect its owner explicitly")
            if path.stat().st_size > args.max_file_bytes:
                raise ValueError("source exceeds max-file-bytes")
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError, ValueError, RuntimeError) as error:
            problems.append(f"{name}: {error}")
            continue
        total += len(raw)
        lines = raw.splitlines()
        if heading is None and match is None:
            titles = "; ".join(title for _, _, title in headings(lines))
            outputs.append((name, [((name, "index"), f"{name}: {len(lines)} lines; headings: {titles}\n")]))
        else:
            for title, ranges in selections(lines, heading, match):
                label = f"{name} [{title}]"
                pieces = [((name, start, end), f"\nSOURCE {name}:{start + 1}-{end}\n" +
                           "\n".join(lines[start:end]) + "\n") for start, end in ranges]
                outputs.append((label, pieces))
    used, emitted, omitted, seen = 0, 0, [], set()
    for label, pieces in outputs:
        output = "".join(body for key, body in pieces if key not in seen)
        if used + len(output) <= args.max_chars:
            print(output, end="")
            used += len(output)
            emitted += 1
            seen.update(key for key, _ in pieces)
        else:
            omitted.append(label)
    print(f"\nSUMMARY files={min(len(paths), args.max_files)} matches={len(outputs)} emitted={emitted} "
          f"omitted={len(omitted)} source_chars={total} excerpt_chars={used} "
          f"unscanned_files={max(0, len(paths) - args.max_files)} errors={len(problems)}")
    for label in omitted[:8]:
        print(f"OMITTED whole section: {label}; narrow selection or raise max-chars")
    for problem in problems[:8]:
        print(f"SKIPPED: {problem}")
    if len(omitted) > 8 or len(problems) > 8:
        print("Additional omissions/errors are counted in SUMMARY; narrow selection for details")
    print("Shared source context is emitted once. Partial retrieval is not a complete rule audit.")
    print("Character counts are not measured model tokens.")
    return bool(problems)


if __name__ == "__main__":
    raise SystemExit(main())
