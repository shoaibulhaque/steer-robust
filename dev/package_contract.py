"""Distribution shape and skill metadata checks for this package, not arbitrary projects."""
import ast
import re
import stat

SKILL_ROOT = ".agents/skills"
SKILLS = ("project-exploration", "change-verification", "runtime-qa", "engineering-change", "statechart", "security-audit")
SCRIPT_ROOT = f"{SKILL_ROOT}/project-exploration/scripts"
SCRIPTS = {f"{SCRIPT_ROOT}/{name}.py" for name in
           ("discover_project", "project_inventory", "inspect_guidance", "guidance_sections")}
GUIDES = {f"Steer-robust/{name}.md" for name in (
    "principles", "design", "efficiency", "state-and-failure", "evolution", "security",
    "verification", "performance", "evaluation", "playbooks", "analyzers")}
EXECUTABLES = {f"{SCRIPT_ROOT}/{name}.py" for name in ("discover_project", "inspect_guidance")}
EXECUTABLES.add(f"{SKILL_ROOT}/statechart/scripts/check.py")
REQUIRED = {*GUIDES, "AGENTS.md", "README.md", "CLAUDE.md", "LICENSE.md", *SCRIPTS,
            f"{SKILL_ROOT}/security-audit/NOTICE.md",
            *(f"{SKILL_ROOT}/security-audit/references/{name}.md" for name in ("findings", "access", "inputs")),
            f"{SKILL_ROOT}/statechart/scripts/check.py",
            f"{SKILL_ROOT}/statechart/references/model-checking.md",
            f"{SKILL_ROOT}/project-exploration/references/discovery.md",
            f"{SKILL_ROOT}/runtime-qa/references/scenarios.md",
            f"{SKILL_ROOT}/runtime-qa/references/evidence.md",
            *(f"{SKILL_ROOT}/{name}/SKILL.md" for name in SKILLS)}


def contents(distribution=False):
    mapping = {name: name for name in REQUIRED}
    if distribution:
        mapping.update({name.replace('.agents/', '.claude/', 1): name
                        for name in REQUIRED if name.startswith('.agents/')})
    return mapping


def mode(name, distribution=False):
    origin = contents(distribution)[name]
    return 0o755 if origin in EXECUTABLES else 0o644


def contract(root, distribution=False):
    errors, resources, names = [], {}, set()
    manifest = contents(distribution)
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append(f"{name}: symlink resources are not distributable")
            continue
        if not path.is_file():
            continue
        names.add(name)
        allowed = name in manifest
        if not allowed:
            errors.append(f"{name}: unexpected distribution file")
        if allowed:
            actual, expected = stat.S_IMODE(path.stat().st_mode), mode(name, distribution)
            bad_mode = actual != expected if distribution else (actual & 0o111) != (expected & 0o111)
            if bad_mode:
                errors.append(f"{name}: incorrect file permissions")
        if distribution and allowed and manifest[name] != name:
            canonical = root / manifest[name]
            if not canonical.is_file() or path.read_bytes() != canonical.read_bytes():
                errors.append(f"{name}: client copy differs from canonical source")
        if path.suffix == ".py":
            try:
                text = path.read_text(encoding="utf-8")
                ast.parse(text, filename=name)
            except (OSError, UnicodeError, SyntaxError) as error:
                errors.append(f"{name}: invalid Python resource: {error}")
                continue
            count = len(text.splitlines())
            resources[name] = {"lines": count, "words": len(text.split())}
    errors.extend(f"missing required resource: {name}" for name in sorted(set(manifest) - names))
    for skill in SKILLS:
        path = root / SKILL_ROOT / skill / "SKILL.md"
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{skill}: unreadable metadata: {error}")
            continue
        front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not front:
            errors.append(f"{skill}: missing YAML frontmatter")
            continue
        fields = dict(re.findall(r"^(name|description):\s*(.+)$", front[1], re.M))
        if fields.get("name") != skill:
            errors.append(f"{skill}: metadata name must match directory")
        description = fields.get("description", "")
        if not description or len(description) > 240:
            errors.append(f"{skill}: description must contain 1..240 characters")
        if re.search(r"\bTODO\b|\[INSERT", text):
            errors.append(f"{skill}: unfinished scaffold")
        if len(text.split()) > 450:
            errors.append(f"{skill}: words exceeds 450")
    return errors, resources
