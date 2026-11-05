"""Distribution shape and skill metadata checks for this package, not arbitrary projects."""
import ast
import re

SKILL_ROOT = ".agents/skills"
SKILLS = ("project-exploration", "change-verification", "runtime-qa")
SCRIPT_ROOT = f"{SKILL_ROOT}/project-exploration/scripts"
SCRIPTS = {f"{SCRIPT_ROOT}/{name}.py" for name in
           ("discover_project", "project_inventory", "inspect_guidance", "guidance_sections")}
REQUIRED = {"AGENTS.md", "README.md", *SCRIPTS,
            f"{SKILL_ROOT}/project-exploration/references/discovery.md",
            f"{SKILL_ROOT}/runtime-qa/references/scenarios.md",
            f"{SKILL_ROOT}/runtime-qa/references/evidence.md",
            *(f"{SKILL_ROOT}/{name}/SKILL.md" for name in SKILLS)}


def contract(root):
    errors, resources, names = [], {}, set()
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append(f"{name}: symlink resources are not distributable")
            continue
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        names.add(name)
        allowed = name in REQUIRED or (name.startswith("Steer-robust/") and path.suffix == ".md")
        if not allowed:
            errors.append(f"{name}: unexpected distribution file")
        if path.suffix == ".py":
            try:
                text = path.read_text(encoding="utf-8")
                ast.parse(text, filename=name)
            except (OSError, UnicodeError, SyntaxError) as error:
                errors.append(f"{name}: invalid Python resource: {error}")
                continue
            count = len(text.splitlines())
            resources[name] = {"lines": count, "words": len(text.split())}
            if count > 120:
                errors.append(f"{name}: {count} lines exceeds 120")
    errors.extend(f"missing required resource: {name}" for name in sorted(REQUIRED - names))
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
