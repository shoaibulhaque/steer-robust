"""Isolated fixture creation; evaluation secrets and graders stay outside worker roots."""
import os
from pathlib import Path
import shutil
import subprocess
from cases import CASES

SOURCE = Path(__file__).resolve().parents[1]


def create(root, case, enabled):
    root.mkdir(parents=True)
    for name, text in CASES[case]["files"].items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    if enabled:
        shutil.copytree(SOURCE / "src", root, dirs_exist_ok=True)
        # The distribution README is instructions for adopters, not fixture task input.
        (root / "README.md").unlink()
    (root / "PROJECT.md").write_text("Use Python standard-library tests. No external dependencies. Do not commit or publish.\n")
    if case == "stateful":
        jar, java = os.environ.get("STEER_TLC_JAR"), os.environ.get("STEER_JAVA")
        text = f"Existing Java: {java}\nExisting TLC jar: {jar}\n" if jar and java else "Java/TLC unavailable; report model checking blocked.\n"
        (root / "TOOLING.md").write_text(text)
    for repo in ([root / "producer", root / "consumer"] if case == "multi" else [root]):
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=Fixture", "-c",
                        "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], check=True)


def environment(home, auth):
    (home / "user").mkdir(parents=True)
    (home / "codex").mkdir()
    (home / "codex/auth.json").symlink_to(auth)
    return {**os.environ, "HOME": str(home / "user"), "CODEX_HOME": str(home / "codex"),
            "PYTHONDONTWRITEBYTECODE": "1"}
