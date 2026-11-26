# Maestro

**Maestro** is a coordinator-driven multi-agent delivery framework. The `maestro-*` folders below are
**ready-to-copy workspaces**: copy one anywhere, put your source code inside, run `claude` (or `codex`)
in it — the agent follows that template's workflow, gates, and identity.

## Pick a template

| Folder | Use it when you want to… | Methodology | Skills |
| --- | --- | --- | --- |
| [`maestro-sdlc/`](maestro-sdlc/) | Build software end-to-end: BA → design → UI/UX prototype → code → real-user QC | spec-driven-development | 237 |
| [`maestro-adlc/`](maestro-adlc/) | **Agent** Development Lifecycle: build agents (`agents/` + `evals/`) with a behavior **eval gate** | eval-driven-ai | 164 |
| [`maestro-enterprise/`](maestro-enterprise/) | Operate governed/production agents: compliance, audit, accountability | enterprise-agent-governance | 168 |
| [`maestro-lite/`](maestro-lite/) | Ship a small tool/prototype fast, minimal ceremony (no specialist advisors) | risk-based-routing | 41 |
| [`maestro-brownfield/`](maestro-brownfield/) | Maintain an EXISTING project (`source/` + `intake/`): deep onboarding, precise tasks, **ask-don't-infer** | risk-based-routing | 227 |
| [`maestro-kiro/`](maestro-kiro/) | Lean **Kiro-native** workspace (`.kiro/` steering + specs + hooks): **ask → do → log**, full-stack Spring Boot · Node · Next · React | direct | 57 |

## One layout rule across every template

```text
.claude/    DEFINITIONS — agents, skills, commands, settings (+ the engine in adlc/brownfield).
            Claude Code write-protects this folder; it changes only in framework maintenance.
.maestro/   WORKSPACE STATE — identity, registries, knowledge, work, memory, runtime
            (+ the engine in sdlc/enterprise/lite). Everything agents write while working.
```

Why: Claude Code refuses Write/Edit inside `.claude/` without a per-call approval, and permission
allow-rules do not lift it (verified on Claude Code 2.1.287). State inside `.claude/` would stall every
workflow step; definitions inside it get write protection for free. Every template ships
`scripts/selftest.py` (links, dangling paths, hooks) and `scripts/behavior-eval.py` (Maestro Way behaviors).

## The Maestro Way — one house style across every template

Every Maestro template works like a disciplined product company with the same recognizable style:

- **House standards** — one explicit quality bar for code (`CS`), UI/UX design (`DS`), architecture
  (`AS`), writing (`WS`), and AI agents (`AG`), with `MUST (floor)` / `MUST` / `SHOULD` levels. Reviews
  cite the ids, so "quality" is checkable instead of taste. → `engine/standards/`
- **Challenge, then commit** (R-028) — agents push back on requests, designs, and code with a steelman,
  evidence, and a better option; the right owner decides; then everyone commits. A claim is never
  reversed under pressure without fresh evidence, and governed reviews run blind in a fresh context.
- **Autonomy with judgment** — each role decides what it owns and records why; only product-visible
  decisions go to the user. Org chart, decision rights, and rituals → `engine/docs/operating-model.md`
- **Learning loop** (R-030) — study before building unfamiliar tech, retro after, and turn every lesson
  into a checkable prevention: inbox → pattern → project convention → house-standard proposal.

Rule ids R-028..R-030 and standard ids are identical in every template. Intensity follows the template:
full in `sdlc`, audit evidence in `enterprise`, `AG`-first in `adlc`, codebase-consistency-first and
ask-don't-infer in `brownfield`, self-check-only in `lite`.

## Use it

```bash
cp -R maestro/maestro-adlc ~/work/my-agent     # copy the template anywhere
cd ~/work/my-agent                              # agents in agents/, eval suites in evals/, host app in app/
claude                                          # /coord to start · /ship for autonomous build-to-done
```

Each template is self-contained and standardized: entry points (`CLAUDE.md`, `AGENTS.md`,
`COMMAND.md`), a purpose-fit agent/skill set, the control plane, and folders for your
code and working artifacts. Ask the agent "who are you" — it answers as that Maestro variant
operating your project.

## Platform (framework source)

[`platform/`](platform/) holds the framework source and the generator. Maintain Maestro there:

```bash
cd platform && python3 scripts/build-variant.py --all   # rebuild the generated maestro-* templates
```

`build-variant.py --all` builds the three generated templates (sdlc, enterprise, lite).
`maestro-adlc/` (`agents/` + `evals/` + `app/`), `maestro-brownfield/` (`source/` + `intake/`), and
`maestro-kiro/` (Kiro-native `.kiro/`) are **independent and hand-maintained** — each has its own
purpose-fit tree and is edited directly, not generated.

Template manifests and the build contract: [platform/variants/README.md](platform/variants/README.md).

## License

MIT — see [LICENSE](LICENSE).
