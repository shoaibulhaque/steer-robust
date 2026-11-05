"""Linux benchmark boundary: hide graders, other trials and temporary answer-building scripts."""
from pathlib import Path
import os
import shutil
import subprocess
from fixtures import SOURCE


def command(argv, trial, env):
    bwrap = shutil.which('bwrap')
    if not bwrap:
        raise RuntimeError('Benchmark requires existing bubblewrap; do not silently expose grading answers')
    args = [bwrap, '--die-with-parent', '--ro-bind', '/', '/', '--dev-bind', '/dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp',
            '--tmpfs', str(SOURCE), '--bind', str(trial), str(trial)]
    for name in ('STEER_TLC_JAR', 'STEER_JAVA'):
        if env.get(name):
            path = Path(env[name]).resolve()
            folder = path.parent if name.endswith('JAR') else path.parent.parent
            args += ['--ro-bind', str(folder), str(folder)]
    return [*args, '--chdir', str(trial/'repo'), '--', *argv]


def verify(trial, env):
    # Checks run inside the same mount policy that will launch Codex, without a model call.
    script = ("from pathlib import Path; "
              f"assert not Path({str(SOURCE/'evals/outcomes.py')!r}).exists(); "
              "assert not Path('/tmp/write-steer-evals.py').exists(); "
              f"assert Path({str(trial/'repo/PROJECT.md')!r}).is_file(); print('grader boundary verified')")
    import sys
    subprocess.run(command([sys.executable, '-c', script], trial, env), env=env,
                   text=True, capture_output=True, check=True, timeout=15)
