---
description: "Resume a task from its recorded state without rediscovering context"
argument-hint: "[task-id]"
---

# /resume-task

## Purpose

Resume a task from its current state without rediscovering context from scratch. Works across
adapters: the previous session may have run in a different tool (R-027).

## Responsible agent

coordinator

## Required rules

```text
00-core-rules.md
01-project-brain-rules.md
11-approval-gates.md
12-artifact-contracts.md
27-session-continuity-rules.md
```

## Workflow

```text
0. Read .maestro/runtime/session-handoff.yaml (skip if absent) and resolve task_id from it when the
   user did not name one. Reconcile against .maestro/runtime/workflow-state.yaml — the state file is
   authoritative; correct the handoff and report the correction.
1. Resolve task_id and task folder under .maestro/work/tasks/<task_id>/.
2. Read task.yaml first; if missing, reconstruct only from artifacts in that same folder.
3. Read task-updates.yaml when present for state/artifact history.
4. Determine current state.
5. Check required artifact for the next transition.
6. Route to the next command.
7. If artifacts are missing, route to the responsible command to recreate them.
8. Rewrite .maestro/runtime/session-handoff.yaml with the current adapter, resolved state,
   next_command, next_owner_agent, and a minimal ordered read_next.
```

## Output format

```yaml
task_id: "<task-id>"
current_state: "<state>"
next_command: "<command>"
missing_artifacts: []
blocked: false
reason: null
previous_adapter: "<claude|codex|other|none>"
read_next: []
```
