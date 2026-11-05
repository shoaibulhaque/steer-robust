# Contributing

Change a demonstrated decision or failure, rather than adding general rules for hypothetical cases.
Keep each rule's trigger, action, preserved guarantee and legitimate exception together.
Reuse the existing owner instead of adding another testing policy or orchestration layer.

## Validation

From the repository root, with Python 3.9+ and Git:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_package.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/build_package.py
```

The package checker validates its authored Markdown subset, budgets, navigation, skill metadata and resources.
The archive tests verify hidden files, extraction, helper execution and repeatable output.
A passing structural check does not prove semantic correctness or live model behavior.
Run the client-provided skill validator too when available; it is not a dependency of this repository.

Keep every authored file within 120 physical lines, root/skill instructions within 450 words,
and shared guides/skill references within 650 words. Avoid unreadable compression to satisfy a limit.
Respect existing repository policy in examples; do not import another project's machine settings or permissions.
State what was tested, inspected and inferred. Behavioral evaluations must report actual conditions and limits.
Never include credentials, private session data or personal filesystem paths in commits or examples.
Do not commit generated ZIPs, caches, raw captures or cloned research repositories.
