# Memory skill quick start

## Upsert (create or update)

```bash
python .github/skills/memory/scripts/memory_store.py upsert \
  --project "FieldOps-Copilot" \
  --topic "trust-evals-design" \
  --text "Use citations, approval gates, and eval regression checks."
```

## Archive (explicit only)

```bash
python .github/skills/memory/scripts/memory_store.py archive \
  --project "FieldOps-Copilot" \
  --topic "trust-evals-design" \
  --reason "Superseded by v2 architecture"
```

## Recover

```bash
python .github/skills/memory/scripts/memory_store.py recover \
  --project "FieldOps-Copilot" \
  --topic "trust-evals-design" \
  --from archive
```
