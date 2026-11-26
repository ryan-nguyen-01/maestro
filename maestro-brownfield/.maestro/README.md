# `.maestro/` — Workspace State

Everything Maestro's agents write while working: product identity, configuration, registries, durable
knowledge, work evidence, memory, history, and local runtime state. Definitions (agents, skills,
commands, engine) live in [`.claude/`](../.claude/README.md), which Claude Code write-protects.

```text
.maestro/
├── project.yaml          Product identity, naming, and component roots
├── methodology.yaml      Methodology routing, overlays, and execution policy
├── config/               Shared model and response configuration
├── registry/             Components, agents, skills, inputs, and artifact addresses
├── knowledge/            Durable project facts, component knowledge, conventions (PC-n)
├── work/                 Initiative, epic, task, subtask, run, bug, and verification evidence
├── memory/
│   ├── project/          Durable patterns, feedback, standard proposals
│   ├── tasks/            Task summaries for cross-session continuation
│   └── sessions/         Local short-term session memory (git-ignored)
├── history/              Event log and timeline
└── runtime/              Local-only active state, telemetry, cache, session handoff (git-ignored)
```

## Read policy

Agents start with `.claude/INSTRUCTIONS.md`, then use the registries and indexes here to open only the
relevant files. The skill registry is the address book for capabilities; the component registry is the
address book for product code.

Shared product knowledge must not be written to `runtime/` or `memory/sessions/` — those are
git-ignored so parallel users do not conflict over chat state or telemetry. Optional domains
(governance, observability, design, decision) are created on first use when an overlay needs them
(`.claude/manifest.yaml` › `optional_domains`). Never store secrets, credentials, or long logs here.
