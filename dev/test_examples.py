"""Execute documented examples; Bash and Node/TypeScript checks are optional."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def blocks(relative, language):
    text = (ROOT / relative).read_text(encoding="utf-8")
    return re.findall(r"```" + language + r"\n(.*?)```", text, re.S)


class ShellExampleTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("bash"), "Bash is unavailable")
    def test_secret_probe_prints_only_presence(self):
        script = blocks("skills/systematic-debugging/SKILL.md", "bash")[0]
        probe = next(line for line in script.splitlines() if "IDENTITY in workflow:" in line)
        for value in (None, "", "SAFE_TEST_CREDENTIAL"):
            with self.subTest(value=value):
                env = {} if value is None else {"IDENTITY": value}
                result = subprocess.run(
                    [shutil.which("bash"), "--noprofile", "--norc", "-c", probe],
                    env=env, capture_output=True, text=True, check=True, timeout=5,
                )
                expected = "SET" if value else "UNSET"
                self.assertEqual(result.stdout, f"IDENTITY in workflow: {expected}\n")
                self.assertEqual(result.stderr, "")


class TypeScriptExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = shutil.which("node")
        if not cls.node:
            raise unittest.SkipTest("Node.js is unavailable")
        version = subprocess.check_output([cls.node, "--version"], text=True, timeout=5)
        if int(version.lstrip("v").split(".")[0]) < 24:
            raise unittest.SkipTest("Node.js 24+ is needed for native TypeScript execution")

    def test_wait_helper_preserves_results_and_sentinels(self):
        source = blocks("skills/systematic-debugging/references/condition-based-waiting.md", "typescript")
        helper = next(block for block in source if "async function waitFor" in block)
        checks = """
import assert from 'node:assert/strict';
assert.equal(await waitFor(() => 0, 'zero', 20), 0);
assert.equal(await waitFor(() => '', 'empty string', 20), '');
for (const pending of [undefined, null, false]) {
  let attempts = 0;
  assert.equal(await waitFor(() => ++attempts < 3 ? pending : 'ready', 'ready', 1000), 'ready');
  assert.equal(attempts, 3);
}
await assert.rejects(waitFor(() => undefined, 'never ready', 0), /Timeout waiting for never ready/);
await assert.rejects(waitFor(() => { throw new Error('worker failed'); }, 'worker'), /worker failed/);
"""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "wait-example.mts"
            path.write_text(helper + checks, encoding="utf-8")
            result = subprocess.run([self.node, str(path)], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_retry_example_typechecks(self):
        compiler = os.environ.get("STEER_TSC")
        command = [self.node, compiler] if compiler else [shutil.which("tsc")]
        if not command[-1]:
            self.skipTest("TypeScript compiler unavailable; set STEER_TSC to an existing tsc.js")
        source = blocks("skills/test-driven-development/SKILL.md", "typescript")
        implementation = next(block for block in source if block.startswith("async function retryOperation"))
        declarations = (
            "declare function test(name: string, run: () => Promise<void>): void;\n"
            "declare function expect(value: unknown): { toBe(expected: unknown): void };\n"
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "retry-example.ts"
            path.write_text(declarations + source[0] + implementation, encoding="utf-8")
            result = subprocess.run(
                [*command, "--strict", "--noEmit", "--target", "ES2020", str(path)],
                cwd=temp, capture_output=True, text=True, timeout=30,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
