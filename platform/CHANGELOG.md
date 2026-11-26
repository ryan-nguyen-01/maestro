# Changelog - maestro

All notable changes to this project are documented here.

Format: `## [version] - YYYY-MM-DD`

---

## [Unreleased]

### Added

- **The Maestro Way (house style)** - Added `.maestro/engine/standards/` with checkable house
  standards for code (CS), UI/UX design (DS, incl. a default "calm, precise, content-first" token
  baseline), architecture (AS), writing (WS), and AI agents (AG), with MUST (floor) / MUST / SHOULD /
  MAY levels and an explicit precedence (floor > project decisions > project conventions > house > taste).
- **R-028 Challenge protocol** - Triggers (purpose, premise, contradiction, risk, standard, complexity,
  value), a fixed challenge shape (steelman, evidence, alternatives, recommendation), stop/flag/note
  severity wired into autopilot hard-stops, decision rights, disagree-and-commit, no sycophantic
  reversal, blind independent review, pre-mortem and alternatives for one-way doors, author second look.
- **R-029 Craft standards** and **R-030 Learning loop** - Standards as the review bar with craft gates
  and `craft-review.template.yaml` records (new Dev Verification critical check R-007-19); study before
  build, pre-flight lessons, `retro.template.md`, promotion ladder up to
  `memory/project/feedback/standard-proposals.md`, prevention over resolution, honest quality signals.
- **Operating model** - `.maestro/engine/docs/operating-model.md`: Maestro as a company (org chart,
  decision-rights matrix, rituals with evidence, escalation ladder). Every agent gained a role-specific
  "House style" section; templates gained `challenges` / `pre_mortem` / `study` fields.

- **Self-tests** - `scripts/selftest.py` (broken links, references to missing control-plane domains,
  hook behavior incl. regression cases, script smoke) runs in every template and after every variant
  build; `scripts/behavior-eval.py` runs headless Claude on a throwaway copy with writes disabled and
  grades three Maestro Way behaviors (over-engineering pushback, false premise, holding the truth).
- **Priority order + R-028-11** - One explicit precedence (safety > mandatory gates > challenges > the
  user's decisions > autonomy > speed) replaces two conflicting "highest priority" labels. "Code now /
  don't ask" compresses gates and challenges into one message with ready options and one question; it
  never skips them. Found by behavior testing: the agent had started coding a 6-service design for a
  one-user todo app because the user said "don't ask".
- **Manifest `writable_boundary` + `optional_domains`** - documents where agents may write and which
  domains are created on first use, so pruned templates have no dangling references.
- **Copy-ready templates** - Every template README opens with a "copy → add your information → talk"
  quick start that says where each kind of information goes for that template (idea, documents, code,
  identity, secrets). `selftest.py --template` (run by every variant build) fails on junk (`.agent/`,
  `.DS_Store`, `__pycache__`), leftover runtime/session/task state, or machine-specific absolute paths;
  builds no longer copy `.agent/` (written by user-global Claude hooks) and `.gitignore` excludes it.
- **Neutral knowledge seed** - Templates used to ship `.maestro/knowledge/project.yaml` describing the
  maestro framework repo itself (`name: maestro`, `workflow-framework`, `confidence: high`, flows with
  `services: maestro`), so a fresh copy "knew" the wrong product until onboarding. Builds now reset the
  project, profile, architecture, and deep-intelligence blocks to an empty seed, and
  `selftest.py --template` fails if a template names a concrete project.
- **Product workspace control plane** - Consolidated framework behavior under `.maestro/` with explicit
  config, registry, knowledge, work, design, decision, memory, history, and local runtime domains.
  Added `docs/`, `apps/`, `services/`, `packages/`, `infra/`, and `tests/` as peer product roots.
- **Adaptive delivery and continuity** - Added `direct`, `assisted`, and `governed` execution modes,
  user/agent/shared verification ownership, Initiative -> Epic -> Task -> Subtask contracts, design
  and decision indexes, checkpoints, continuation handoffs, and task/session/project memory layers.
- **Collision-resistant initialization** - `/maestro-init` appends an idempotent `.maestro/INSTRUCTIONS.md`
  entry block, preserves existing `CLAUDE.md` and `AGENTS.md`, ignores local runtime/session state,
  supports `--attach` and `--sync`, and does not ignore the product `services/` root.
- **Methodology playbooks** - Added official governance docs for Risk-Based Workflow Routing,
  Spec-Driven Development, Enterprise Agent Governance, and Eval-Driven AI Development, plus a
  selection matrix wired into `.maestro/methodology.yaml`,
  `.maestro/registry/artifacts.yaml`, docs indexes, and `/maestro-init` scaffolding.
- **Enterprise Agent Governance operating model** - Applied production-agent governance concepts:
  accountable owner, governance policy, mission, behavior contract, autonomy policy, agent definition,
  eval suite, audit log, interaction protocol, 9-stage lifecycle, pilot readiness, and artifact roots
  under `docs/governance/enterprise-agent-governance/`.
- **Spec-driven workflow upgrades** - Added document precedence tiers, hash-based conflict detection
  for generated files, and two-axis task classification through execution mode and run requirements.
- **Claude Code plugin wrapper** - Packaged Claude agents, skills, commands, and hooks as an additive
  plugin generated by `scripts/build-plugin.py`.
- **Codex plugin and prompts** - Added `scripts/build-codex-plugin.py` and
  `scripts/build-codex-prompts.py` so Codex can install skills and mirror workflow slash commands.
- **Specialist advisor layer** - Added 19 advisor-only specialist agents for architecture, product,
  quality/security, data/AI, operations/devex, and research/QA. Workflow agents can request their
  advisory artifacts without giving them implementation authority.
- **Hook guardrails** - Added deterministic scope, secret, and destructive-command hooks for Claude and
  Cursor-style enforcement paths.
- **Skill discovery layer** - Added `scripts/build-skill-catalog.py`, category frontmatter, machine
  indexes, and human-readable skill catalogs for 237 skills.
- **Model routing and activity dashboard** - Added `.maestro/config/model-routing.yaml`,
  `.maestro/runtime/agent-activity.yaml`, `.maestro/config/response-ui.yaml`, `scripts/status-dashboard.py`,
  and `scripts/agent-activity.py`.
- **Architecture health check** - Added `scripts/architecture-health-check.py` to validate counts,
  entrypoints, model routing, response UI, plugin drift, skill catalog drift, and deterministic
  control-plane assumptions.

### Changed

- **maestro-adlc / maestro-brownfield: workspace state moved out of `.claude/`** - Claude Code refuses
  Write/Edit inside `.claude/` without per-call approval and allow-rules do not lift it (verified on
  2.1.287), so runtime state there stalled every workflow write. `.claude/` now holds definitions
  (agents, skills, commands, engine, settings, manifest); `.maestro/` holds identity, config, registries,
  knowledge, work, memory, history, runtime — the same state location as every generated template.
- **Variant build** drops index lines (list items / table rows) that link into pruned folders.

### Removed

- **Workspace mode command** - Removed the command-based switch/repair flow. Product identity now
  lives in `.maestro/project.yaml`, and workflow progress lives in `.maestro/runtime/workflow-state.yaml`.
- **Legacy root placeholder folders** - Removed obsolete `memory/`, `state/`, duplicate handover
  folders, old handoff templates, and example runtime task folders.

### Fixed

- `scope-guard.py` gated framework/state writes whose path contained a source token
  (`.maestro/work/tasks/<id>/tests/…`, `.claude/skills/<x>/lib/…`) and classified tokens in the ABSOLUTE
  path, so a checkout under e.g. `~/src/` gated every file. It now classifies the project-relative path
  and never gates `.maestro/`, `.claude/`, `.codex/`, `scripts/`, `docs/`, `deliverables/`.
- Broken links: engine README → skill registry, agent catalog → specialists catalog, platform README →
  templates/LICENSE, AGENTS.md → runtime files that only exist at runtime.
- `status-dashboard.py` compact render crashed when both a value and its fallback field were missing,
  which failed `architecture-health-check.py --strict` on a fresh workspace.
- **Current count drift** - Synchronized docs and health-check expectations to 33 agents, 237 skills,
  27 rules, 62 templates, and 22 commands.
- **Runtime semantics** - Reframed `.maestro/runtime/` as local-only active state, telemetry, cache, and
  reports. Durable knowledge now lives under `.maestro/knowledge/`, and work artifacts live under `.maestro/work/`.
- **Component-root semantics** - Clarified that `apps/`, `services/`, `packages/`, `infra/`, and
  `tests/` are product roots, not framework-owned folders.
- **Bug artifact contract** - Clarified task-local bug indexes versus canonical bug details under
  `.maestro/work/bugs/`.
- **Coding feedback loop** - Added root cause, prevention rule, regression check, and recurrence keys so
  recurring implementation mistakes can be promoted into durable memory.
- **English documentation policy** - Converted framework-facing documentation to English for cleaner AI
  interpretation while keeping conversation language user-led.

---

## [1.7.0] - 2026-05-18

### Added

- **`inputs/` folder convention** - Added a root-level location for user-provided PRDs, HLDs, ADRs,
  OpenAPI specs, domain glossaries, runbooks, and other references.
- **Incremental input refresh** - Added `/onboard --refresh inputs`, `/sync-memory --scan --inputs`,
  file hash checks, and deleted-file cleanup for input-derived memory.
- **Input index** - Added `.maestro/registry/inputs.yaml` as the index agents read before opening raw input
  files.
- **General AI entrypoint** - Added `AGENTS.md` for non-Claude tools such as Codex, Cursor, Aider,
  Gemini, Copilot, and similar agents.
- **Solution Architect workflow agent** - Added an optional architecture review gate for
  cross-service, API, data, event, security, and infrastructure risk.
- **Cross-cutting coders** - Added `coder-infra` and `coder-database` as built-in coders for shared
  infrastructure and database work.
- **Tool-specific entrypoints** - Added Codex, Cursor, Gemini, and Copilot instruction files so tools
  can share the same workflow contracts.
- **Tool-native value add** - Added Codex config, Cursor rules, Cursor hooks, and per-tool setup
  documentation.
- **Runtime/data separation** - Moved tool-neutral runtime data out of Claude-specific folders so all
  supported tools can read the same project state.

### Changed

- Tightened policy gates based on real workflow evidence: `DEV_DONE` requires dev verification, QC pass
  cannot be claimed while blockers or manual retest gaps remain, and policy checks inspect artifact
  consistency.
- Added fast-track exceptions, architecture review trigger fields, skill budget rules, deterministic
  skill selection, and drift-detection bookkeeping.
- Standardized task IDs as `TASK-YYYYMMDD-NNN-slug`.
- Consolidated coder outputs into `coder-results.yaml`.

### Removed

- Removed legacy placeholder roots and duplicate handover layers from earlier migration phases.

### Fixed

- Standardized folder semantics and count documentation.

---

## [1.6.0] - 2026-05-17

### Changed

- Split runtime context into clearer memory, service control, state, task, bug, and handover areas.
- Added `memory/index.yaml` so agents read a routing index before opening detailed memory files.
- Extended `/onboard` and `/sync-memory` with refresh flows.
- Updated agents, rules, templates, setup docs, folder guide, and validator scripts for the updated
  memory/service/state structure.

---

## [1.5.2] - 2026-04-17

### Added

- Added a Task Analysis -> User Approval Gate before Coder Leader for governed work.
- Added QC Delivery Report generation after QC completes.
- Added example task artifacts and updated workflow narrative examples.

### Documentation

- Updated workflow reference, architecture guide, visual flow diagrams, agent catalog, folder guide, and
  SVG diagrams to include the approval gate and QC delivery report.

---

## [1.5.1] - 2026-04-17

### Added

- Added FAQ and troubleshooting material.
- Added customization guidance for custom skills and registry updates.
- Added example end-to-end JWT Authentication workflow artifacts.
- Added coder-to-leader handoff obligations and templates.

---

## [1.5.0] - 2026-04-17

### Added

- Added architecture guide, workflow reference, agent catalog, skill guide, customization guide, and an
  end-to-end demo task template.
- Added default framework configuration in `.claude/settings.json`.

### Changed

- Added upgrade, subtree, and post-install validation guidance.

### Fixed

- Improved SVG diagram viewBox, font consistency, dark theme styling, and cross-references.

---

## [1.4.0] - 2026-03-31

### Removed

- Removed hooks, git hooks, root blueprints, and obsolete handoff skills from the minimal repository
  distribution.

### Changed

- Synchronized documentation and skills with the no-hooks, no-handoff-file, inline-blueprint model.

---

## [1.3.1] - 2026-03-31

### Added

- Added an active handoff convention for orchestrator, analyst, and context injection workflows.

### Changed

- Updated orchestration, analysis, context, injection, and guideline documents to use the handoff
  convention.

---

## [1.3.0] - 2026-03-31

### Added

- Added token and context policy material.
- Added context-keeper dirty-flag handling.

### Changed

- Updated context-first read order, progressive escalation, injection budgets, and dirty-flag policy.

---

## [1.2.0] - 2026-03-31

### Added

- Added seven concrete blueprint files for CRUD modules, authentication, file upload, payments,
  real-time features, search/filter, and caching.

### Changed

- Documented blueprint files as source of truth for the blueprint skill.

---

## [1.1.0] - 2026-03-31

### Added

- Added Git hooks, English keyword routing, decision rules for product and data agents, and validation
  checks for context maintenance.

### Changed

- Restructured architecture skills into Core, API, and Conditional Architecture tiers.
- Removed duplicate builder skill catalog content.
- Clarified execution models for reporter and context-keeper agents.

### Fixed

- Added missing decision rules for planning, release delays, pipeline design, and incidents.
- Reduced oversized duplicated content in builder skill documentation.

---

## [1.0.0] - 2026-02-01

### Added

- Initial release with 20 core agents and 106 skills.
- Agent definitions for orchestration, onboarding, building, architecture, business analysis, product,
  design, coding, review, testing, security, documentation, migration, QA, performance, SRE, data,
  context keeping, and reporting.
- Skill library across languages, frameworks, databases, authentication, testing, UI, DevOps,
  architecture, observability, and tooling.
- Claude routing system, setup guide, feedback loop, blueprints, context system, and generated-agent
  conventions.
