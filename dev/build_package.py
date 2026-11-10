#!/usr/bin/env python3
"""Build the portable instruction kit from an explicit allowlist; no runtime tooling."""
from pathlib import Path
import io
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.7.0-candidate"
NAME = f"steer-robust-v{VERSION}"
SKILLS = ("architecture-engineering", "refactoring", "systematic-debugging",
          "test-driven-development", "change-verification", "security-engineering")
FILES = (
    "AGENTS.md", "README.md", "LICENSE", "EVAL_PLAN.md", "research/README.md",
    "templates/project-instructions.md",
    *(f"skills/{name}/SKILL.md" for name in SKILLS),
    "skills/test-driven-development/references/writing-good-tests.md",
    "skills/architecture-engineering/references/greenfield-design.md",
    "skills/architecture-engineering/references/brownfield-evolution.md",
    "skills/architecture-engineering/references/integration-and-migration.md",
    "skills/architecture-engineering/references/change-locality.md",
    "skills/architecture-engineering/references/architecture-evaluation.md",
    "skills/architecture-engineering/references/architecture-plan-casebook.md",
    "skills/architecture-engineering/references/design-decisions.md",
    "skills/architecture-engineering/references/state-and-failure.md",
    "skills/architecture-engineering/references/performance-decisions.md",
    "skills/refactoring/references/dependency-breaking.md",
    "skills/change-verification/references/verification-boundaries.md",
    "skills/architecture-engineering/LICENSE.txt",
    "skills/architecture-engineering/NOTICE.md",
    "skills/test-driven-development/LICENSE.txt",
    "skills/systematic-debugging/references/root-cause-tracing.md",
    "skills/systematic-debugging/references/condition-based-waiting.md",
    "skills/systematic-debugging/references/defense-in-depth.md",
    "skills/systematic-debugging/LICENSE.txt",
    "skills/security-engineering/references/threat-modeling.md",
    "skills/security-engineering/references/security-controls-and-assets.md",
    "skills/security-engineering/references/stack-guidance.md",
    "skills/security-engineering/references/api-and-parser-boundaries.md",
    "skills/security-engineering/references/ai-application-boundaries.md",
    "skills/security-engineering/references/build-and-secrets-integrity.md",
    "skills/security-engineering/references/runtime-and-observability.md",
    "skills/security-engineering/references/audit-evidence-and-coverage.md",
    "skills/security-engineering/references/threat-informed-defense.md",
    "skills/security-engineering/references/security-intelligence-and-untrusted-sources.md",
    "skills/security-engineering/LICENSE.txt", "skills/security-engineering/NOTICE.md",
    "research/skill-adaptation-review.md",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate():
    """Check required files and this kit's simple metadata/link syntax, not agent behavior."""
    require({p.name for p in (ROOT / "skills").iterdir()} == set(SKILLS), "Unexpected skill")
    require(len(FILES) == len(set(FILES)), "Duplicate distribution entry")
    for name in SKILLS:
        folder = ROOT / "skills" / name
        require(not folder.is_symlink(), f"Linked skill directory: {name}")
        expected = {p for p in FILES if p.startswith(f"skills/{name}/")}
        resources = list(folder.rglob("*"))
        require(not any(p.is_symlink() for p in resources), f"Linked skill resource: {name}")
        actual = {p.relative_to(ROOT).as_posix() for p in resources if p.is_file()}
        require(actual == expected, f"Missing or unlisted skill resources: {name}")
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (\"[^\n]+\")\n---\n", text)
        require(match and match[1] == name, f"Invalid metadata: {name}")
        require(bool(json.loads(match[2]).strip()), f"Empty description: {name}")
    for name in FILES:
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), f"Missing or linked resource: {name}")
        path.resolve().relative_to(ROOT)
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        require(text.count("```") % 2 == 0, f"Unclosed code fence: {name}")
        for target in re.findall(r"\]\(([^\s)]+)\)", text):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#", target):
                continue
            destination = (path.parent / target.split("#", 1)[0]).resolve()
            relative = destination.relative_to(ROOT).as_posix()
            require(relative in FILES and destination.is_file(), f"Unpackaged link: {name}: {target}")


def archive():
    validate()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for name in sorted(FILES):
            entry = zipfile.ZipInfo(f"{NAME}/{name}", date_time=(2020, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(entry, (ROOT / name).read_bytes(), compresslevel=9)
    return buffer.getvalue()


if __name__ == "__main__":
    data = archive()
    destination = ROOT / "dist" / f"{NAME}.zip"
    destination.parent.mkdir(exist_ok=True)
    destination.write_bytes(data)
    print(f"Validated and built {destination} ({len(FILES)} files; {len(data)} bytes)")
