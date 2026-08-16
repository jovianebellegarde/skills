---
name: memory-log
description: >-
  Private memory manager for project/topic knowledge. Upserts existing memories
  or creates new ones, archives only on explicit request, and recovers archived
  or trashed memories when needed.
compatibility: >-
  Repository-local skill for Copilot workflows. Uses filesystem-backed memory
  records under .github/memories.
---

# Memory Log Skill

Use this skill to manage durable memory records by `project` and `topic`.

## Scope

- Root memory store: `.github/memories/`
- Active memories: `.github/memories/active/`
- Archived memories: `.github/memories/archive/`
- Recoverable deletions: `.github/memories/trash/`

## Behavior rules

1. **Upsert (default)**
   - Check for existing active memory by project/topic.
   - If found: update it (append update entry + refresh metadata).
   - If not found: create a new memory record.

2. **Archive**
   - Archive only when the user explicitly asks to archive.
   - Move memory from `active` to `archive` with timestamped filename.
   - Never silently archive.

3. **Recover**
   - Recover memory from `archive` or `trash` back to `active`.
   - Preserve recovery provenance in metadata.

4. **Delete safety**
   - Do not hard-delete memory files.
   - Move deletions to `trash` so accidental deletes are recoverable.

## Command interface

Run the helper script:

```bash
python .github/skills/memory-log/scripts/memory_store.py <command> [flags]
```

Commands:

- `upsert --project <name> --topic <name> --text "<content>"`
- `archive --project <name> --topic <name> --reason "<why>"`
- `recover --project <name> --topic <name> [--from archive|trash]`
- `delete --project <name> --topic <name> --reason "<why>"`
- `show --project <name> --topic <name>`
- `list [--project <name>] [--state active|archive|trash|all]`

## Invocation guidance

- Treat `upsert` as the default action for “remember this” style requests.
- Require explicit user intent for `archive` and `delete`.
- Prefer `recover` if a memory was removed by mistake.
