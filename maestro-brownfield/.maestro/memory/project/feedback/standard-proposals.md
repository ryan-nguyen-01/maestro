# House Standard Proposals

Lessons that would apply to ANY project, not just this one (R-030-05). Memory Update writes them here;
they change `.claude/engine/standards/` only through user-approved framework maintenance (R-029-08).

## Template

```yaml
- id: SP-0001
  proposed_standard_id: "CS-37"        # next free id in the target standard
  target: code|design|architecture|writing|agents
  level: MUST|SHOULD
  text: "One checkable sentence."
  evidence:                            # >= 2 incidents, or 1 severe
    - ".maestro/work/tasks/<task-id>/retro.md#went-wrong-1"
  prevention: "The check this enables (test / lint / hook / checklist item)."
  status: proposed|accepted|rejected
  decided_by: null
  updated_at: 2026-11-26
```

## Entries
