# Memory-log skill quick start

## Upsert (create or update)

```bash
python .github/skills/memory-log/scripts/memory_store.py upsert \
  --project "FieldOps-Copilot" \
  --topic "trust-evals-design" \
  --text "Use citations, approval gates, and eval regression checks."
```

## Archive (explicit only)

```bash
python .github/skills/memory-log/scripts/memory_store.py archive \
  --project "FieldOps-Copilot" \
  --topic "trust-evals-design" \
  --reason "Superseded by v2 architecture"
```

## Recover

```bash
python .github/skills/memory-log/scripts/memory_store.py recover \
  --project "FieldOps-Copilot" \
  --topic "trust-evals-design" \
  --from archive
```

## Duplicate prevention

- If the same content is saved again for the same project/topic, the skill performs a no-op update.
- If the same content is saved under a new topic but already exists in active memory for that project, the skill deduplicates into the existing memory instead of creating a duplicate file.
