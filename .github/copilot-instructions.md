# Copilot instructions for the skills repository

This repository stores reusable Agent Skills and private memory data for personal Copilot workflows.

## Repository layout

- Skills live under `.github/skills/<skill-name>/`.
- Each skill must include `.github/skills/<skill-name>/SKILL.md`.
- Memory records live under `.github/memories/`.
- `.github/memories/active/`, `.github/memories/archive/`, and `.github/memories/trash/` are data stores managed by the `log-memory` skill.

## Skill authoring rules

- Follow the Agent Skills format: YAML frontmatter with `name` and `description`, followed by Markdown instructions.
- The `name` value must match the parent directory name and use lowercase letters, numbers, and hyphens only.
- Keep skill descriptions specific about when the skill should be used so Copilot can load the right skill on demand.
- Prefer small, focused skills over broad instruction dumps.
- Reference any helper scripts, examples, or resources from `SKILL.md` using relative Markdown links.

## Safety rules

- Do not commit secrets, tokens, credentials, or private environment files.
- Do not hard-delete memory records unless the user explicitly asks. Prefer the `log-memory` skill's recoverable delete flow.
- Do not modify `.github/memories/` content unless the user explicitly asks to save, update, archive, recover, or delete memory.

## Validation

- For Markdown-only skill edits, review the changed `SKILL.md` files for valid frontmatter and clear invocation guidance.
- For script-backed skills, run the smallest relevant command or test that verifies the script still works.
