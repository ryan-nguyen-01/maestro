# `.claude` Changelog

## 2.0.0 — Claude Code native alignment (2026-10-07)

Breaking layout change plus alignment with Claude Code 2.1.28x (validated on 2.1.287):

- Control plane merged from `.maestro/` into `.claude/`; agents flattened to `.claude/agents/<name>.agent.md`
  (specialists keep `category:` frontmatter instead of subfolders).
- `AGENTS.md` is now the single source of shared instructions (identity, ADLC profile, resume, rules,
  flows). `CLAUDE.md` is a thin adapter: `@AGENTS.md` import + Claude-only notes. Claude Code reads
  `AGENTS.md` natively only when no `CLAUDE.md` exists, so the import is the supported way to share it;
  it is never loaded twice. `.claude/INSTRUCTIONS.md` keeps only the control-plane read order.
  Auto markers became HTML comments so they no longer inject stray H1s into context.
- Subagents: tool `Task` renamed to `Agent` (coordinator, coder-leader); every workflow agent and
  built-in coder now carries `model` + `effort` frontmatter mirroring `model-routing.yaml`; specialists
  gained `effort`. Agent templates updated so generated coders/specialists follow suit.
  `model-routing.yaml.adapter_binding` documents how each adapter applies the profiles.
- Commands: all 22 have `description` / `argument-hint` frontmatter for the `/` menu. The commands
  index moved to `.claude/engine/docs/command-index.md` (a `README.md` in `.claude/commands/` would
  register as `/README`). `build-codex-prompts.py` strips the frontmatter so Codex mirrors are unchanged.
- `scope-guard.py`: classifies the project-relative path (the absolute path previously gated framework
  files whenever the workspace lived under a dir such as `src/`), never gates `.claude/`, `.codex/`,
  `scripts/`, `docs/`, `deliverables/`, and now gates the ADLC work roots `agents/` and `evals/` (R-017-02).
- Health check: follows `@path` imports for entrypoint checks; new `check_claude_native` (CLAUDE.md
  imports AGENTS.md, no `Task` tool, agent model frontmatter, command descriptions, no commands README);
  removed the dead `.claude-plugin` wrapper check.
- Engine rules stay in `.claude/engine/rules/` (on demand) — deliberately not `.claude/rules/`, which
  Claude Code would auto-load every session.
- Stale references fixed: 20 (not 19) specialists, `<category>/` paths, SETUP.md mentions, truncated
  Plugin section, per-tool table (Claude Code does run hooks).

## Framework maintenance fast path

Added explicit framework maintenance behavior so the product-development control plane can be maintained without running product-component onboarding:

- `target_scope: framework` treats `NEED_ONBOARDING`, empty component registries, and seed brain values as expected for framework-only work.
- Coordinator classifies `target_scope` before broad brain/service reads.
- Framework maintenance sets `requires_onboarding: false` unless application source under `services/<service-name>/` is involved.
- Trivial framework maintenance can use lightweight fast-track evidence instead of full task artifacts.
- `/policy-check snapshot` uses the `workflow-policy` agent checklist for migration/snapshot validation.
- Workflow Policy validates artifact-only snapshots without requiring `services/` or Python/Node/script dependencies, catches Code Done/QC Done gate bypasses, and offers dry-run-first mode repair.
- Coordinator, Task Analysis, Coder Leader, Dev Verification, QC Handoff, and QC Runner now use conditional reads so framework maintenance does not load project brain, registry, component registry, test policy, or task artifacts unnecessarily.
- Runtime skill loading now starts from `skill-registry.yaml` and must not scan/read all of `.claude/skills/**`.
- Cross-tool entrypoints were aligned for Codex, Cursor, Gemini, and GitHub Copilot.
- Seed runtime files now describe `services/` as the application-source workspace and `.runtime/context` as the service control plane.
- Cursor hooks now enforce architecture approval, standard plan artifacts, active coder write scope, and broader destructive-command blocking before source edits or shell execution.
- Workflow references now include artifact snapshot policy checks and approval gates R-011-10b through R-011-14.
- Context economy layer added: project/component archetypes, signature-first onboarding, project_profile, component profile.context_hints, context_economy, and task context_plan.
- Planning/coding now blocks when context confidence is low or service/test/contract ownership is unresolved.
- Cursor source-edit gating now fails closed, covers common universal source roots, requires context_plan for all product-component edits including fast-track, and requires lightweight service-assignments.yaml for product-component fast-track.
- Runtime/template approval_gates now include the full R-011 approval surface, service-brain no longer encourages full service-root reads, and docs counts were synced.
- Model routing and observability added: model-routing.yaml maps agents to stable model profiles, agent-activity.yaml backs `/status`, `scripts/status-dashboard.py` provides a terminal mirror, and R-015 governs model fallback plus ETA reporting.
- Response UI contract added: response-ui.yaml defines compact/concise/dashboard/models/dev/review/policy markdown layouts for Claude, Codex, Cursor, Gemini, and Copilot, while documenting that native client chrome remains tool-owned.
- Status artifacts added: `python3 scripts/status-dashboard.py --mode dashboard --write` generates `.maestro/runtime/reports/status.md` and `.maestro/runtime/reports/status.html` from workflow state, model routing, agent activity, and response UI.
- 9.5+ hardening helpers added: `scripts/agent-activity.py` updates adapter telemetry and `scripts/architecture-health-check.py --strict` catches deterministic drift without replacing agent-native `/policy-check`.
- Scoped model overrides added: `model-routing.yaml.model_overrides` supports safe model switching without editing agent files or removing stable profiles.
- `/status` terminal mirror now reports Project Brain freshness and selected response UI mode, model-routing template ships the complete runtime seed agent map, docs treat `services/` as an optional empty local clone workspace, and architecture health checks catch these drift classes.
- Bug routing contract clarified: task-level `bugs.yaml` is an index only, canonical bug details must live under `.maestro/work/bugs/blockers/` or `.maestro/work/bugs/non-blockers/`, and health checks now detect missing canonical bug artifacts referenced by task indexes.
- Coding error feedback loop added: confirmed implementation errors carry root cause, prevention rule, regression check, and recurrence key; Memory Update promotes durable lessons into feedback patterns/anti-patterns; future Task Analysis and Coder Leader context packs include relevant prevention items.
- Status HTML now renders as a GitHub README-style card with tabs, hero banner, metric cards, and raw status audit text; health checks verify the generated HTML style marker.

## Dynamic agent architecture installed

Replaced static agent and technology skill set with a project-aware workflow:

```text
Coordinator
Onboarding
Agent Factory
Task Analysis
Coder Leader
Generated Service Coders
Dev Verification
QC Handoff
QC Runner
Bug Router
Memory Update
Workflow Policy
```

Project brain now starts in `NEED_ONBOARDING` state.

## Skill registry hardening

Implemented review fixes without running project onboarding:

```text
settings.json and settings.local.json are now valid JSON objects.
workflow.md duplicate skill-composition section removed.
rules/README.md rule 14 formatting fixed.
.maestro/registry/skills.yaml added as machine-readable skill selection source of truth.
Agent Factory and /create-coders now use skill-registry.yaml before external-skills.md.
High-risk and failed external skills are represented as explicit registry gates.
```

## Deep onboarding and reuse enforcement

Added deeper onboarding support without scanning the real project:

- project-brain.yaml now has deep_project_intelligence placeholder sections.
- project-brain and service-brain templates now include reusable assets, coding flow, business flows, reuse rules, anti-patterns, evidence, and confidence fields.
- task-analysis template now includes reuse_and_convention_analysis.
- dev-verification template now includes reuse_and_convention_check.
- memory-update template now includes reuse_and_convention_memory_updates.
- Onboarding, Task Analysis, Coder Leader, Service Coder, Dev Verification, and Memory Update instructions now enforce reuse-before-create behavior.
- Added docs/deep-onboarding.md as the human-readable standard.
[session-end] 2026-05-18T06:27:46Z
[session-end] 2026-05-18T06:39:46Z
[session-end] 2026-05-18T06:47:21Z
[session-end] 2026-05-18T06:49:16Z
[session-end] 2026-05-18T07:06:43Z
[session-end] 2026-05-18T07:15:32Z
[session-end] 2026-05-18T07:25:14Z
[session-end] 2026-06-02T04:18:49Z
[session-end] 2026-06-02T04:41:22Z
[session-end] 2026-06-02T06:20:22Z
[session-end] 2026-06-02T08:25:09Z
[session-end] 2026-06-03T01:17:40Z
[session-end] 2026-06-03T01:27:03Z
[session-end] 2026-06-06T09:04:26Z
[session-end] 2026-06-06T10:46:38Z
[session-end] 2026-06-06T11:08:53Z
[session-end] 2026-06-06T11:10:34Z
