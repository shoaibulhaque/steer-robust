#!/usr/bin/env python3
"""Build a validated distribution including selected skills and read-only helpers."""
from pathlib import Path
import json
import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
from validate_package import validate
from package_contract import SCRIPT_ROOT, SKILL_ROOT, SKILLS, contents, mode


def smoke(root):
    scripts = root / SCRIPT_ROOT
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    discovery = subprocess.run([sys.executable, str(scripts / "discover_project.py"), str(root)],
                               text=True, capture_output=True, check=True, env=env, timeout=30)
    data = json.loads(discovery.stdout)
    expected = {"AGENTS.md", *(f"{SKILL_ROOT}/{skill}/SKILL.md" for skill in SKILLS)}
    missing = expected - {item["path"] for item in data["candidates"]}
    if missing:
        raise SystemExit(f"Extracted discovery helper missed instructions/skills: {sorted(missing)}")
    excerpt = subprocess.run([sys.executable, str(scripts / "inspect_guidance.py"), str(root),
                              "--glob", "AGENTS.md", "--heading", "^Authority and scope$"],
                             text=True, capture_output=True, check=True, env=env, timeout=30)
    if "explicit approval" not in excerpt.stdout or "omitted=0" not in excerpt.stdout:
        raise SystemExit("Extracted retrieval helper lost required scope context")


def main():
    source = Path(__file__).resolve().parents[1]
    package = source / "src"
    errors, stats = validate(package)
    if errors:
        raise SystemExit("\n".join(errors))
    manifest = contents(distribution=True)
    output = source / "dist" / "Steer-robust.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w") as archive:
        for name in sorted(manifest):
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100000 | mode(name, True)) << 16
            archive.writestr(info, (package / manifest[name]).read_bytes())
    with TemporaryDirectory() as temporary, ZipFile(output) as archive:
        if set(archive.namelist()) != set(manifest):
            raise SystemExit("Archive contents differ from the validated package")
        archive.extractall(temporary)
        for info in archive.infolist():
            (Path(temporary) / info.filename).chmod(info.external_attr >> 16 & 0o777)
        errors, _ = validate(Path(temporary), distribution=True)
        if errors:
            raise SystemExit("Extracted archive failed validation: " + "; ".join(errors))
        for name in manifest:
            if (Path(temporary) / name).read_bytes() != (package / manifest[name]).read_bytes():
                raise SystemExit(f"Archive differs from source: {name}")
        smoke(Path(temporary))
    print(f"Built and verified {output}: {len(manifest)} files, {output.stat().st_size} bytes")


if __name__ == "__main__":
    main()
