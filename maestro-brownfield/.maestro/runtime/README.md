# Local Runtime

This directory contains machine- and session-local execution state. Its contents are ignored by
Git except for this file.

Typical files:

- `workflow-state.yaml`: active task, mode, state machine position, and local approvals.
- `session-handoff.yaml`: adapter-neutral resume pointer (R-027) — see engine/docs/session-continuity.md.
- `agent-activity.yaml`: transient activity and telemetry.
- `active-context.yaml`: current session, subtask, checkpoint, and verification owner.
- `cache/sync.json`: local SHA-256 baseline used to guard framework-owned files during sync.
- `cache/`, `locks/`, `reports/`: generated local data.

Canonical operating domains live in `.claude/engine/` (workflow, rules, templates) and `.maestro/work/`.
Shared facts belong in `.maestro/knowledge/`, registries in `.maestro/registry/`, and auditable work
evidence in `.maestro/work/`.
