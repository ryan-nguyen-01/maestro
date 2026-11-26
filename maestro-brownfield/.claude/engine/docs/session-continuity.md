# Session Continuity Across Adapters

Canonical, adapter-neutral contract for pausing work in one harness (Claude Code, Codex CLI,
Cursor, Copilot, …) and resuming it in another without losing workflow position.

Every entrypoint file (`CLAUDE.md`, `AGENTS.md`, `.codex/AGENTS.md`, `.claude/INSTRUCTIONS.md`)
points here instead of restating the sequence, so the protocol cannot drift per tool.

## 1. Why this exists

`.claude/` (definitions) + `.maestro/` (state) are the single control plane; adapters are interchangeable front-ends. An adapter that
starts a session with no memory of the previous one must be able to answer four questions from
files alone:

```text
1. Where am I?         current workflow state + active task/run
2. What just happened?  last completed step and the artifact it produced
3. What is next?        next command and the agent that owns it
4. What do I read?      the minimal, ordered file list to continue
```

For brownfield work this matters even more than for greenfield: ask-don't-infer means a session
that forgets what it already asked (and was told) will re-ask the user or silently re-guess —
exactly the failure mode this protocol exists to prevent.

## 2. Source of truth

| Question | File | Authority |
|---|---|---|
| Workflow position | `.maestro/runtime/workflow-state.yaml` | **Authoritative.** State machine, active task/run, gates. |
| Continuation brief | `.maestro/runtime/session-handoff.yaml` | Derived pointer: last adapter, last step, next command, read list. |
| Task evidence | `.maestro/work/tasks/<task-id>/` | Authoritative for artifacts and their contents. |
| Durable handoff | `.maestro/memory/tasks/<task-id>/handoff.md` | Cross-session narrative, survives runtime resets. |

Conflict rule: when `session-handoff.yaml` disagrees with `workflow-state.yaml` or task artifacts,
**the authoritative sources win** and the handoff is rewritten. Never advance a gate on the
strength of the handoff pointer alone.

Both files live under `.maestro/runtime/` (git-ignored, machine-local). They persist across adapter
switches on the same machine. For a switch across machines or clones, the durable handoff in
`.maestro/memory/tasks/<task-id>/handoff.md` plus committed task artifacts are the carrier.

## 3. RESUME sequence — run at the start of every session, in every adapter

```text
R1. Read .claude/engine/workflow.md                     (rules of the machine)
R2. Read .maestro/runtime/session-handoff.yaml           (where we left off; skip if absent)
R3. Read .maestro/runtime/workflow-state.yaml            (authoritative position)
R4. Reconcile R2 against R3:
      - state/task/run mismatch  -> trust R3, rewrite R2, report the correction
      - handoff missing/empty     -> reconstruct from R3 + task artifacts, then write R2
      - both missing              -> current_state = NEW, route to /coord
R5. Read only the files in session-handoff.read_next (plus the responsible agent definition
      at .claude/agents/<agent>.agent.md). Do not broad-scan the workspace.
R6. Announce the resume banner, then continue with progress.next_command.
```

Resume banner (one line, before any work):

```text
Resume: {state} | task {task_id|none} | run {run_id|none} | last: {last_completed_step} | next: {next_command} | prev adapter: {adapter.last}
```

Shortcut for humans and for adapters that can run commands:

```bash
python3 scripts/session-handoff.py --show            # renders the resume brief
python3 scripts/session-handoff.py --check           # reports drift vs workflow-state.yaml
```

## 4. HANDOFF sequence — run before stopping, switching tools, or ending a phase

```text
H1. Finish or checkpoint the current unit of work; write its artifact under
      .maestro/work/tasks/<task-id>/.
H2. Update .maestro/runtime/workflow-state.yaml (state, active_task_id, active_run_id, reason).
H3. Update .maestro/runtime/session-handoff.yaml: adapter, last_completed_step, last_artifact,
      next_command, next_owner_agent, read_next, blocked/blocker, open_questions.
H4. For work that must survive a runtime reset or a different machine, also write
      .maestro/memory/tasks/<task-id>/handoff.md from the continuation-handoff template.
```

Adapters that can run commands should use the helper instead of hand-editing YAML:

```bash
python3 scripts/session-handoff.py \
  --adapter codex --state IN_DEV --task TASK-20260804-001-login \
  --step "coder-leader assigned auth + api" \
  --artifact .maestro/work/tasks/TASK-20260804-001-login/service-assignments.yaml \
  --next /dev --owner coder-leader \
  --read .maestro/work/tasks/TASK-20260804-001-login/implementation-plan.yaml
```

## 5. Adapter capability matrix

Same policy, different enforcement. Know which column you are in before trusting automation.

| Capability | Claude Code | Codex CLI | Manual fallback |
|---|---|---|---|
| Auto-loads `.claude/agents/*.agent.md` as subagents | yes | no | read the agent file explicitly before acting as that agent |
| Slash commands from `.claude/commands/` | yes | only after installing `.codex/prompts/` | treat the command name as an intent and execute `.claude/commands/<name>.md` |
| Skills from `.claude/skills/` | yes | via `codex plugin` (`scripts/build-codex-plugin.py`) | read `.claude/skills/<name>/SKILL.md` directly |
| PreToolUse hooks (`scope-guard`, `secret-guard`, `destructive-guard`) | yes | no | enforce R-000 / R-006 / R-013 / R-011-07 by hand |
| Writes `session-handoff.yaml` | required | required | `scripts/session-handoff.py` |

Because `.claude/agents/` is a **flat** directory, every adapter discovers agents the same way:
one glob over `.claude/agents/*.agent.md`. Class comes from metadata, not folders — `category:`
frontmatter marks a specialist advisor, a `coder-` prefix marks a coder, the remaining files are
the 12 workflow agents.

## 6. Invariants

```text
C-01: An adapter must not start product work before completing the RESUME sequence.
C-02: workflow-state.yaml is authoritative; session-handoff.yaml is a pointer, never a gate.
C-03: Every phase transition writes both files before the adapter reports the phase done.
C-04: read_next lists only files needed for the next step — it is a context budget, not an index.
C-05: No secrets, credentials, or long logs in the handoff; it is prompt-visible by design.
C-06: Switching adapters never changes execution mode, verification owner, or approval gates.
```

## 7. Related

- Rule file: [`../rules/27-session-continuity-rules.md`](../rules/27-session-continuity-rules.md)
- Template: [`../templates/session-handoff.template.yaml`](../templates/session-handoff.template.yaml)
- Durable narrative template: [`../templates/continuation-handoff.template.md`](../templates/continuation-handoff.template.md)
- Task-level resume contract: [`../../commands/resume-task.md`](../../commands/resume-task.md)
