#!/usr/bin/env python3
"""Check the authored Markdown subset: local links/anchors, navigation and size budgets."""
import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from package_contract import SKILL_ROOT, SKILLS, contract


def markdown(text):
    """Ignore fenced examples; recognize ATX headings and simple inline links."""
    body, anchors, seen, fence = [], set(), {}, None
    for line in text.splitlines():
        token = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if token:
            mark = token.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence) and not line[token.end():].strip():
                fence = None
            continue
        if fence:
            continue
        body.append(line)
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            slug = re.sub(r"[^\w\- ]", "", heading[1].lower()).replace(" ", "-")
            suffix = seen.get(slug, 0)
            seen[slug] = suffix + 1
            anchors.add(f"{slug}-{suffix}" if suffix else slug)
    links = re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", "\n".join(body))
    return links, anchors


def validate(root, distribution=False):
    root = root.resolve()
    errors, stats = contract(root, distribution)
    docs = {}
    for path in sorted(root.rglob("*.md")):
        name = path.relative_to(root).as_posix()
        if not path.resolve().is_relative_to(root):
            errors.append(f"{name}: file escapes package")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{name}: {error}")
            continue
        docs[name] = (text, *markdown(text))
        lines, words = len(text.splitlines()), len(text.split())
        stats[name] = {"lines": lines, "words": words}
        budget = 450 if name == "AGENTS.md" else 650 if name.startswith("Steer-robust/") or "/references/" in name else None
        if budget and words > budget:
            errors.append(f"{name}: {words} words exceeds {budget}")
    if "AGENTS.md" not in docs:
        errors.append("missing AGENTS.md")
    bridge = docs.get("CLAUDE.md", ("", [], set()))[0]
    if "@AGENTS.md" not in bridge.splitlines():
        errors.append("CLAUDE.md: missing canonical AGENTS import")
    guides = {name for name in docs if name.startswith("Steer-robust/")}
    if not guides:
        errors.append("missing reference guides")
    root_targets = set()
    for name, (text, links, _) in docs.items():
        if name in guides and not re.search(r"^Read when\b", text, re.M):
            errors.append(f"{name}: missing Read when trigger")
        for target in links:
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme in {"https", "http", "mailto"}:
                continue
            if parsed.scheme or parsed.netloc:
                errors.append(f"{name}: non-portable link {target}")
                continue
            path = Path(unquote(parsed.path))
            resolved = (root / name).parent / path if parsed.path else root / name
            resolved = resolved.resolve()
            if path.is_absolute() or not resolved.is_relative_to(root):
                errors.append(f"{name}: non-portable link {target}")
                continue
            key = resolved.relative_to(root).as_posix()
            if not resolved.exists():
                errors.append(f"{name}: missing target {target}")
            if parsed.fragment and (key not in docs or unquote(parsed.fragment) not in docs[key][2]):
                errors.append(f"{name}: missing anchor {target}")
            if name == "AGENTS.md":
                root_targets.add(key)
    for name in sorted(guides - root_targets):
        errors.append(f"{name}: not directly linked from AGENTS.md")
    for skill in SKILLS:
        if f"{SKILL_ROOT}/{skill}/SKILL.md" not in root_targets:
            errors.append(f"{skill}: not directly linked from AGENTS.md")
    return errors, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", nargs="?", type=Path, default=Path(__file__).resolve().parents[1] / "src")
    parser.add_argument("--distribution", action="store_true", help="validate generated native-client copies too")
    args = parser.parse_args()
    errors, stats = validate(args.package, args.distribution)
    for name, counts in stats.items():
        print(f"{name}: {counts['lines']} lines, {counts['words']} words")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"{'FAIL' if errors else 'PASS'}: {len(stats)} authored files; {len(errors)} structural errors")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
