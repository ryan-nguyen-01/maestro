<!--
Maintainers: shared instructions live in AGENTS.md (single source for Claude Code, Codex, and other
AGENTS.md readers). This file only imports it and adds Claude Code specifics — never copy shared
rules here. Claude Code >= 2.1.277 reads AGENTS.md natively only when no CLAUDE.md exists; because
this file exists, the @AGENTS.md import below is what loads it (and it is never read twice, whatever
the "Project instructions" setting). HTML comments like this one are stripped from Claude's context.
-->
@AGENTS.md

# Claude Code adapter

Everything above (from AGENTS.md) applies. This section covers only what is specific to Claude Code.

## Precedence over the user-global `~/.claude/CLAUDE.md`

Claude Code concatenates the user-global file and this project's files; it does not drop either.
**On conflict, this project wins.** Only the agents in AGENTS.md exist here. Names that a global
file may define route like this:

```text
agent-orchestrator, product-manager, agent-discovery,
agent-documenter, site-reliability-eng., agent-reporter   → coordinator (/status for reporting)
agent-analyst                                              → task-analysis
agent-migrator                                             → coordinator (via task-analysis)
agent-designer                                             → coordinator (UI task → coder-leader after analysis)
agent-coder-*                                              → coder-leader (assigns the right coder)
agent-reviewer                                             → coder-leader (code-quality review, R-005-09)
agent-tester                                               → generated coder or qc-runner, by phase
agent-security, performance-engineer                      → coordinator (task gets critical_checks)
quality-assurance                                          → qc-runner / qc-handoff
agent-context-keeper                                       → memory-update
business-analyst, data-engineer (as workflow agents)       → coordinator (they exist here only as
                                                             advisors invoked inside the pipeline)
```

Global routing aliases (`sa:`, `ba:`, `qa:`, `pm:`, `sec:`, `sre:`, `dev:`) are **disabled** here;
natural language or the slash commands in AGENTS.md are the interface. A global "Bootstrap /
`.agent/` onboarding" step never applies — this workspace's session-resume protocol replaces it.

## Native discovery

| Surface | Location | How it is used |
| --- | --- | --- |
| Subagents | `.claude/agents/*.agent.md` (flat) | Spawn with the **Agent** tool, `subagent_type` = frontmatter `name`. `model` + `effort` frontmatter mirror the profile in `.maestro/config/model-routing.yaml`; a scoped override there is passed as the per-invocation `model`, never by editing agent files. `README.md` / `SPECIALISTS.md` have no frontmatter and are not loaded as agents. |
| Skills | `.claude/skills/<name>/SKILL.md` | Auto-invoked by description or `/name`. Pick by domain from [skill-catalog.md](.claude/engine/docs/skill-catalog.md) — never scan the folder. |
| Commands | `.claude/commands/<name>.md` | `/name`; each file has a `description` frontmatter for the `/` menu. Index: [COMMAND.md](COMMAND.md). |
| Settings + hooks | `.claude/settings.json` | Shared, committed. Personal overrides go in `.claude/settings.local.json` (git-ignored). |

Model profile → Claude alias (aliases track the newest model of each family; pin a full ID such as
`claude-opus-5-5` only through `model_overrides`):

```text
deep_reasoning                      → opus    effort high
coding · coding_planner · verification → sonnet effort medium
fast_router · memory_light          → sonnet  effort low
```

Response UI is defined in `.maestro/config/response-ui.yaml`: status, model report, review, dev
summary, policy report, and final answers follow its mode unless the user asks for a format. It
shapes markdown/text and the status artifact, not the client's native panels.

The 28 engine rules intentionally stay in `.claude/engine/rules/` (read on demand by the agents that
own them). Do not move them into `.claude/rules/`: Claude Code auto-loads every file there into each
session, which would break the context-economy budget (R-000).

## Hooks (deterministic guardrails)

PreToolUse hooks in `.claude/settings.json`, backed by `scripts/hooks/`, turn key rules into hard blocks:

- `scope-guard.py` — direct/assisted/governed source-edit contracts and governed coder scope on the
  work roots `agents/`, `evals/`, `app/`, `tests/`, … (R-000, R-006). Framework files are not gated.
- `secret-guard.py` — blocks secret material in writes (R-013).
- `destructive-guard.py` — blocks destructive Bash commands (R-011-07).

Runtime controls (no code edits): `MAESTRO_HOOK_PROFILE=minimal|standard|strict` (default `standard`),
`MAESTRO_DISABLED_HOOKS=comma,ids`. Contract: [R-017](.claude/engine/rules/17-hook-enforcement-rules.md).
`/access` switches tool-permission posture only; it never disables these hooks or workflow gates (R-011-14).

## Session handoff from Claude

Record `--adapter claude` when writing the handoff:
`python3 scripts/session-handoff.py --adapter claude --state <STATE> --next </cmd> --owner <agent> --step "<done>" --artifact <path> --read <files...>`.
Status mirror for any client: `python3 scripts/status-dashboard.py --mode dashboard` (telemetry in
`.maestro/runtime/agent-activity.yaml`).
