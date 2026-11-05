#!/usr/bin/env python3
"""Run optional TLC safety checking; record exact evidence and render its trace."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def states(output):
    blocks = re.split(r"(?m)^State (\d+):[^\n]*\n", output)
    result = []
    for i in range(1, len(blocks), 2):
        values = []
        for line in blocks[i + 1].splitlines():
            if line.startswith("/\\ ") or (not values and re.match(r"^\w+ = ", line)):
                values.append(line.removeprefix("/\\ "))
            elif values and (not line.strip() or re.match(r"^(?:\d+ states|Finished|Progress|Model checking)", line)):
                break
            elif values:
                values.append(line)
        if values:
            result.append({"step": int(blocks[i]), "values": "\n".join(values)})
    return result


def mermaid(trace):
    # Numeric entities stop source values from injecting Mermaid syntax.
    def escape(value):
        return "".join(c if c.isalnum() or c in " =,_-" else f"#{ord(c)};" for c in value)
    lines = ["stateDiagram-v2", "    [*] --> S1"]
    for i, state in enumerate(trace, 1):
        lines.append(f'    state "{escape(state["values"])}" as S{i}')
        if i > 1:
            lines.append(f"    S{i - 1} --> S{i}: step {state['step']}")
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("spec", type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--jar", required=True, type=Path)
    p.add_argument("--java", default="java")
    p.add_argument("--search", choices=["bfs", "iterative"], default="bfs")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--timeout", type=int, default=60)
    a = p.parse_args()
    if a.timeout < 1 or not all(x.is_file() for x in (a.spec, a.config, a.jar)):
        p.error("spec/config/jar must exist and timeout must be positive")
    if a.out.exists():
        p.error("out must be a fresh directory")
    a.out.mkdir(parents=True)
    cmd = [a.java, "-Xmx256m", "-cp", str(a.jar.resolve()), "tlc2.TLC", "-workers", "1",
           "-metadir", str((a.out / "states").resolve()), "-config", str(a.config.resolve()), str(a.spec.resolve())]
    if a.search == "iterative":
        cmd[cmd.index("-metadir"):cmd.index("-metadir")] = ["-dfid", "1024"]
    status, code, output = "tool_error", None, ""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout, cwd=a.spec.resolve().parent)
        code, output = r.returncode, r.stdout + r.stderr
        if code == 0 and "Model checking completed. No error has been found." in output:
            status = "passed_bounded_model"
        elif re.search(r"Invariant .* is violated", output):
            status = "safety_counterexample"
    except subprocess.TimeoutExpired as error:
        status = "timeout"
        output = (error.stdout or b"").decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
    except OSError as error:
        output = str(error)
    trace = states(output) if status == "safety_counterexample" else []
    if status == "safety_counterexample" and not trace:
        status = "unparsed_counterexample"
    hashes = {str(x.resolve()): hashlib.sha256(x.read_bytes()).hexdigest() for x in (a.spec, a.config, a.jar)}
    report = {"status": status, "exit_code": code, "command": cmd, "sha256": hashes,
              "trace": trace, "shortest": bool(trace), "scope": f"bounded {a.search} safety model, one worker"}
    (a.out / "tlc.out").write_text(output)
    (a.out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    if trace:
        (a.out / "trace.mmd").write_text(mermaid(trace))
    print(json.dumps({"status": status, "trace_states": len(trace)}))
    return 0 if status == "passed_bounded_model" else 1


if __name__ == "__main__":
    raise SystemExit(main())
