# Modification and License Notice

This skill combines the user-supplied OpenAI `security-best-practices` and `security-threat-model`
skills, distributed under the [Apache License 2.0](LICENSE.txt). Upstream source:
[openai/skills](https://github.com/openai/skills).

Changes made by Steer Robust:

- `SKILL.md`: rewritten. Merges discovery and mode selection, routes each stack to its manual, adds
  finding classification, a worked example and fix rules, and revises reporting and clarification to
  follow the actual request.
- `references/threat-modeling.md`: rewritten from the threat-model skill and its prompt template. Keeps
  the eight-stage workflow, discovery checklist, likelihood × impact scoring and output contract;
  replaces the mandatory pause with targeted questions and writes a file only when asked.
- `references/security-controls-and-assets.md`: extended with evidence guidance, personal-data lifetime
  and an example.
- The ten `references/*-security.md` stack manuals retain their security rules. Trailing whitespace
  was normalized in the Express, general frontend JavaScript, React, and Django manuals.

Changes made 2026-11-06. The supplied archive remains unchanged. This modified version is not an official
OpenAI product or endorsement.
