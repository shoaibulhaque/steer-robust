"""Read-only filename inventory and heuristic categories; no rule interpretation."""
import os
from pathlib import Path
import re
import subprocess

EXCLUDED = {".git", "node_modules", "vendor", ".venv", "venv", "__pycache__",
            ".next", ".nuxt", ".cache", "target", "dist", "build", "coverage"}
AGENT_NAMES = {"agents.md", "agents.override.md", "claude.md", "gemini.md"}
MANIFESTS = {"package.json", "pyproject.toml", "cargo.toml", "go.mod", "gemfile",
             "pom.xml", "build.gradle", "composer.json", "mix.exs", "pubspec.yaml",
             "makefile", "justfile", "taskfile.yml", "tox.ini", ".tool-versions"}


def git(root, *args):
    return subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15, check=False)


def category(path):
    name, parts = path.name.lower(), tuple(p.lower() for p in path.parts)
    joined = "/".join(parts)
    if name in AGENT_NAMES or name == ".cursorrules":
        return "instructions"
    if name == "skill.md":
        return "skill"
    if any(s in joined for s in (".claude/rules/", ".cursor/rules/", ".agents/rules/",
                                ".github/instructions/")) or name == "copilot-instructions.md":
        return "conditional-rule"
    if name == "codeowners":
        return "ownership"
    if any(s in joined for s in ("pull_request_template", "issue_template", "merge_request_templates")):
        return "template"
    if ".github/workflows/" in joined or name in {".gitlab-ci.yml", "azure-pipelines.yml", "jenkinsfile"}:
        return "ci"
    if name in MANIFESTS or name.startswith(("requirements", ".python-version", ".node-version", ".nvmrc")):
        return "toolchain"
    if path.suffix.lower() in {".md", ".mdx", ".rst", ".txt"} and re.search(
            r"readme|index|contribut|architect|overview|onboard|setup|develop|test|security|policy|style|guide", name):
        return "documentation"
    return None


def inventory(root, maximum, extra=()):
    warnings, paths, excluded = [], [], 0
    mode, head, truncated = "filesystem", None, False
    try:
        result = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
        if result.returncode == 0:
            mode = "git-index"
            paths = sorted(set(os.fsdecode(p) for p in result.stdout.split(b"\0") if p))
            revision = git(root, "rev-parse", "--verify", "HEAD")
            head = revision.stdout.decode().strip() if revision.returncode == 0 else None
        else:
            warnings.append("Git index unavailable; filesystem fallback does not interpret ignore files")
    except (OSError, subprocess.SubprocessError) as error:
        mode, paths = "filesystem", []
        warnings.append(f"Git unavailable ({type(error).__name__}); filesystem fallback ignores ignore files")
    if mode == "filesystem":
        def walk_error(error):
            warnings.append(f"walk failed: {error}")
        for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
            excluded += sum(d in EXCLUDED or (Path(directory) / d).is_symlink() for d in dirs)
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(directory) / d).is_symlink())
            for name in sorted(files):
                paths.append((Path(directory) / name).relative_to(root).as_posix())
                if len(paths) > maximum:
                    truncated = True
                    break
            if truncated:
                break
    paths = list(dict.fromkeys([*extra, *paths]))
    truncated = truncated or len(paths) > maximum
    records, seen = [], set()
    for name in paths[:maximum]:
        path = Path(name)
        if any(part in EXCLUDED for part in path.parts):
            excluded += 1
            continue
        full = root / path
        try:
            if not full.resolve().is_relative_to(root) or any(
                    p.is_symlink() for p in (full, *full.parents) if p != root and p.is_relative_to(root)):
                warnings.append(f"symlink/escaping path skipped: {name}")
                continue
            if not full.is_file():
                warnings.append(f"indexed path missing or not a regular file: {name}")
                continue
        except (OSError, RuntimeError) as error:
            warnings.append(f"unreadable path {name}: {error}")
            continue
        kind = category(path)
        if kind and name not in seen:
            records.append({"path": name, "kind": kind})
            seen.add(name)
    return {"mode": mode, "head": head, "scanned_files": min(len(paths), maximum),
            "scan_limit_reached": truncated, "excluded_entries": excluded,
            "warnings": warnings, "candidates": records}
