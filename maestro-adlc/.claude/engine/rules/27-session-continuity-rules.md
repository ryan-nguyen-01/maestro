# R-027: Session Continuity Across Adapters

## Applies to

Every agent, in every adapter (Claude Code, Codex CLI, Cursor, Copilot). Coordinator enforces;
each phase-owning agent writes its own handoff. The defect class this prevents: a user switches
harness mid-delivery and the new session rediscovers context by scanning the repo, re-asks settled
questions, or resumes at the wrong phase.

Protocol reference: `.claude/engine/docs/session-continuity.md`.

## Rules

```text
R-027-01: RESUME BEFORE WORK. Every session, in every adapter, runs the RESUME sequence (R1–R6 of
  session-continuity.md) before processing the first user request. No product work, no gate
  transition, and no file write before the resume banner is reported.
R-027-02: AUTHORITY ORDER IS FIXED. .maestro/runtime/workflow-state.yaml is authoritative for workflow
  position; task artifacts are authoritative for evidence; .maestro/runtime/session-handoff.yaml is a
  derived pointer. On conflict, trust the authoritative source, rewrite the pointer, and report the
  correction. Never advance a state or approve a gate on the pointer alone.
R-027-03: WRITE BOTH FILES AT EVERY PHASE BOUNDARY. A phase is not done until workflow-state.yaml and
  session-handoff.yaml both reflect it. session-handoff.yaml must carry: adapter, current_state,
  active task/run, last_completed_step, last_artifact, next_command, next_owner_agent, read_next.
R-027-04: READ_NEXT IS A CONTEXT BUDGET. It lists only the files the next step actually needs, in
  order. It is not an index of the workspace, and an incoming adapter must not broad-scan beyond it
  without a stated trigger (R-000 context economy).
R-027-05: DURABLE HANDOFF FOR NON-LOCAL CONTINUATION. When work may resume after a runtime reset, on
  another machine, or after a long gap, also write .maestro/memory/tasks/<task-id>/handoff.md from
  continuation-handoff.template.md. Runtime files are machine-local and must never be the only carrier.
R-027-06: ADAPTER SWITCH IS NOT A POLICY RESET. Changing harness must not change execution mode,
  verification owner, approval gates, methodology, or coder write scope. An adapter without hooks
  (Codex, Copilot) enforces R-000/R-006/R-013/R-011-07 manually and says so in the resume banner.
R-027-07: CAPABILITY DEGRADATION IS DECLARED, NOT SILENT. When the active adapter cannot auto-load
  agents, commands, skills, or hooks, state the fallback being used (read the agent/command/skill file
  directly) instead of skipping the contract.
R-027-08: THE HANDOFF IS PROMPT-VISIBLE. No secrets, credentials, tokens, raw cookies, customer data,
  or long logs in session-handoff.yaml or handoff.md (R-013). Reference artifact paths instead.
R-027-09: STALE POINTER IS A BLOCKER, NOT A GUESS. If session-handoff.yaml points at a task folder,
  run, or artifact that does not exist, do not infer intent — reconstruct from workflow-state.yaml and
  the task folder, or route to /resume-task and /policy-check.
```

## Evidence

```text
- Resume banner in the first reply of the session.
- session-handoff.yaml.adapter.updated_at newer than the last phase transition.
- next_command matching the state machine's allowed transition from current_state.
```

## Helper

```bash
python3 scripts/session-handoff.py --show     # resume brief
python3 scripts/session-handoff.py --check    # drift vs workflow-state.yaml
python3 scripts/session-handoff.py --adapter <name> --state <STATE> --next </cmd> ...
```

The helper is a convenience for adapters that can run commands. It is not a dependency: an agent
with file access satisfies this rule by reading and writing the YAML directly.
