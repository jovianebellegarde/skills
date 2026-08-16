# skills

Private-to-public skills repository for reusable Copilot workflows.

## Included skill

### Log-memory skill

Path: `.github/skills/log-memory/`

This skill provides durable memory management by `project` and `topic` with:

- create-or-update (`upsert`)
- explicit archiving (`archive`)
- recovery from archive/trash (`recover`)
- safe delete to trash (`delete`)

## Memory storage layout

The log-memory skill stores records in:

- `.github/memories/active/`
- `.github/memories/archive/`
- `.github/memories/trash/`

The repository tracks only folder placeholders (`.gitkeep`) so personal memory content is not published by default.

## Quick usage

```bash
python .github/skills/log-memory/scripts/memory_store.py upsert \
  --project "FieldOps-Copilot" \
  --topic "trust-evals" \
  --text "Use citations, approval gates, and regression evals."
```
