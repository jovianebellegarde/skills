---
name: log-memory
description: >-
  Private memory manager for project/topic knowledge. Upserts existing memories
  or creates new ones, archives only on explicit request, and recovers archived
  or trashed memories when needed.
compatibility: >-
  Repository-local skill for Copilot workflows. Uses filesystem-backed memory
  records under .github/memories.
---

# Log-memory Skill

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
   - Duplicate guard: if incoming content already exists in the project's active memory body, do not create a duplicate record.

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
python .github/skills/log-memory/scripts/memory_store.py <command> [flags]
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
- Prevent duplicates by default: merge into existing project memory when content is already represented.
- Before saving a long-form project memory, normalize the content into a structured shape instead of storing a raw note dump.

## Memory detail standard (default quality bar)

When saving or updating memory, prefer high-detail structured captures over short summaries.

Default include list:

- Decision context and why it was chosen
- Problem framing and user/workflow framing
- Detailed implementation shape (components, layers, responsibilities)
- Trust/safety and evaluation requirements
- Concrete examples and edge cases
- Suggested stack/layout when relevant
- Interview-defensibility or explainability points when relevant
- Clear next-step readiness notes

If the user explicitly asks for brief memory, follow that override. Otherwise, store the fuller version.

## Structured memory standard (preferred default)

When the memory is about a project, product direction, architecture, trust design, evaluation strategy, or operating decisions, rewrite the content into a clean structured record before saving it.

Prefer this section order when the information is available:

1. **Project**
   - Project or initiative name
   - One-sentence identity/value proposition

2. **Goal**
   - What outcome the project is trying to create
   - What success looks like

3. **Users / workflow**
   - Who the system helps
   - What workflow or operating pain it improves

4. **Product thesis**
   - Why this approach matters
   - Why it is better than a generic assistant or unstructured workflow

5. **Trust rules**
   - Citation/grounding requirements
   - Clarifying-question requirements
   - Refusal boundaries
   - Human-approval gates

6. **Eval targets**
   - What should be tested
   - Pass/fail expectations
   - Important failure modes or regressions to watch

7. **Architecture**
   - Main system components
   - Responsibilities of each layer
   - Important integrations or data flow assumptions

8. **Decisions made**
   - Key decisions already taken
   - Why they were chosen

9. **Open questions**
   - What remains unresolved
   - What should not be assumed yet

10. **Next steps**
    - Concrete build or research steps
    - What should happen next in the project

### Formatting guidance

- Prefer concise bullets under each heading over dense paragraphs.
- Preserve the user's meaning, but clean up wording and merge duplicates.
- Omit empty sections rather than inventing content.
- If the content is just a narrow fact or small preference, keep it simple and do not force the full template.
- If updating an existing memory, keep the same structure and revise the relevant sections instead of appending another unstructured dump.

### Example use

Instead of saving:

- "FieldOps is an FDE project, trust matters, use citations and approval, add evals, maybe use retrieval and audit logs."

Prefer saving:

- **Project:** FieldOps Copilot
- **Goal:** Help field teams prepare customer actions from trusted internal context.
- **Trust rules:** Cite sources, ask clarifying questions when context is missing, require approval for risky actions.
- **Eval targets:** Fail if the system invents customer history or makes unsupported recommendations.
- **Architecture:** Retrieval + policy gate + approval path + audit log.
- **Open questions:** Should MVP be draft-only or take actions directly?
