"""Task definitions fixed independently of worker responses; no package wording in prompts."""
CASES = {
    "bug": {
        "prompt": "Fix get_document so one tenant cannot fetch another tenant's document. Preserve valid reads and missing-document behavior. Add appropriate regression proof.",
        "files": {"store.py": "DOCS = {1: {'tenant': 'a', 'text': 'hello'}}\ndef get_document(tenant, key):\n    return DOCS.get(key)\n"},
        "skills": ["engineering-change", "change-verification"],
        "guides": ["principles", "design", "security", "verification"]},
    "abstraction": {
        "prompt": "Support pickup orders with zero shipping cost in quote(total, mode='delivery'). Delivery remains 5. This is a small shop with only these two modes; keep the design proportionate. Verify behavior.",
        "files": {"shipping.py": "def quote(total, mode='delivery'):\n    return total + 5\n"},
        "skills": ["engineering-change", "change-verification"],
        "guides": ["principles", "design", "verification"]},
    "verification": {
        "prompt": "The ledger CLI claims --dry-run but still creates its output file. Fix it and provide meaningful regression verification through the CLI, preserving the normal write path.",
        "files": {"ledger.py": "import argparse\nfrom pathlib import Path\np = argparse.ArgumentParser()\np.add_argument('--out', required=True)\np.add_argument('--dry-run', action='store_true')\na = p.parse_args()\nPath(a.out).write_text('committed\\n')\nprint('ok')\n"},
        "skills": ["engineering-change", "change-verification", "runtime-qa"],
        "guides": ["principles", "design", "verification"]},
    "lever": {
        "prompt": "Migrate the service JSON files in configs/ from endpoint to base_url at the top level. Preserve other fields, nested endpoint keys and arbitrary text. Complete the existing tools/migrate.py so reviewers can rerun the migration on a directory safely, including after partial completion. Verify a second run.",
        "files": {"tools/migrate.py": "import sys\nfrom pathlib import Path\n# CLI: python tools/migrate.py DIRECTORY. Complete the migration here.\n", **{
            f"configs/service{i}.json": '{"endpoint":"https://example.test/' + str(i) + '","nested":{"endpoint":"preserve"},"note":"endpoint"}\n'
            for i in range(16)}},
        "skills": ["engineering-change", "change-verification"],
        "guides": ["principles", "design", "efficiency", "verification"]},
    "multi": {
        "prompt": "Coordinate producer/ and consumer/, which are separate Git repositories. Add emit(amount, currency='USD') and render(record) so report output is '<amount> <currency>'. Preserve old records without currency as USD, fractional amounts and input immutability. Verify both repositories.",
        "files": {"producer/api.py": "def emit(amount):\n    return {'amount': amount}\n",
                  "consumer/report.py": "def render(record):\n    return str(record['amount']) + ' USD'\n",
                  "producer/AGENTS.md": "Read CONTRACT.md before editing. Use Python standard library tests.\n",
                  "producer/CONTRACT.md": "Amounts preserve fractional precision; do not round or cast to integer.\n",
                  "consumer/AGENTS.md": "Read CONTRACT.md before editing. Use Python standard library tests.\n",
                  "consumer/CONTRACT.md": "Rendering must not mutate its input record. Missing currency means USD.\n"},
        "skills": ["engineering-change", "change-verification"],
        "guides": ["principles", "design", "evolution", "verification"]},
    "stateful": {
        "prompt": "Fix stale callbacks: a Lease callback captured before retire() must reject after retirement without increasing calls. First establish a valid callback works. Analyze the capture/retire/call ordering with a bounded TLA+ model and show its counterexample as Mermaid; replay it in a real regression test. Existing optional model-checking dependencies are described in TOOLING.md. Keep spec/configs, raw model-checker outputs and Mermaid under evidence/ for review. Do not download/install anything.",
        "files": {"lease.py": "class Lease:\n    def __init__(self):\n        self.active = True\n        self.calls = 0\n    def callback(self):\n        allowed = self.active\n        def call():\n            if not allowed: raise RuntimeError('retired')\n            self.calls += 1\n        return call\n    def retire(self):\n        self.active = False\n"},
        "skills": ["engineering-change", "change-verification", "statechart"],
        "guides": ["principles", "design", "state-and-failure", "verification"]},
}

from extended_cases import EXTENDED
CASES.update(EXTENDED)
