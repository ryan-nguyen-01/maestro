# Maestro Control-Plane Read Order

This repository splits its control plane in two: `.claude/` holds the definitions (agents, skills,
commands, engine — write-protected by Claude Code) and `.maestro/` holds the workspace state agents write
(identity, registries, knowledge, work, memory, runtime). Identity, the ADLC
variant profile, and the session-resume protocol live in [AGENTS.md](../AGENTS.md) — the single
source of shared instructions — and are not repeated here. This file is the stable map of what to
read, in which order, once a session has resumed.

Read in this order:

1. `.maestro/project.yaml` for product identity, naming, and component roots.
2. `.maestro/methodology.yaml` for execution mode, methodology overlays, and verification ownership.
3. `.claude/engine/workflow.md` and `.claude/engine/rules/` — the canonical control plane for workflow, policy, guardrail, and template domains.
4. `.maestro/registry/skills.yaml` before loading any skill.
5. `.maestro/registry/components.yaml` before locating product code.
6. `.maestro/knowledge/index.yaml` before opening broader project knowledge.
7. `.maestro/work/index.yaml`, `.maestro/work/runs/index.yaml`, and active task/run artifacts when work is tracked.
8. `.maestro/observability/index.yaml` before creating trace, eval, report, or audit evidence.
9. `.maestro/runtime/workflow-state.yaml` and `.maestro/runtime/session-handoff.yaml` for local session state and cross-adapter resume ([session-continuity.md](engine/docs/session-continuity.md), rule `R-027`).

Agent definitions belong in `agents/` (mission, tools, prompts, memory, knowledge); the host
application in `app/`; behavior eval suites in `evals/`; cross-cutting tests in `tests/`. Official
product documents belong in `docs/`. Do not store secrets or long logs in `.claude/` or `.maestro/`.

Use `direct` mode for fast user-verified work, `assisted` for resumable bounded work, and
`governed` for high-risk or cross-component delivery. Apply Spec-Driven Development, Eval-Driven AI
Development, or Enterprise Agent Governance as overlays when the task requires traceability,
eval-driven AI, or governed autonomous operation. When a conversation grows too long, write a
checkpoint and continuation handoff before starting a new session.

Work the Maestro Way: the house standards in `.claude/engine/standards/` are the quality bar for
code, design, architecture, writing, and AI agents (R-029); challenge material problems with evidence and
a better option, let the owner decide, then commit fully — and never reverse a position under pushback
without fresh evidence (R-028); "code now / don't ask" compresses gates and challenges into one message
with ready options and one question, never skips them (R-028-11); study before building and turn every lesson into a checkable prevention
(R-030). Decision rights and rituals: `.claude/engine/docs/operating-model.md`.

Prefer run-centric operation for non-trivial work: a task describes intent, a run records one attempt,
checkpoints preserve progress, traces and evals support quality claims, approvals record human gates,
and memory updates preserve reusable learning.
