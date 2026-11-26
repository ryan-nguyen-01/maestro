# Rules Index

Rules are mandatory policy files. Agents and commands must follow these rules before acting.

## Rule loading principle

```text
Read only the rule files required by the active command or agent.
If a rule conflicts with an agent file, the rule wins.
If a rule conflicts with workflow.md, workflow.md defines the state machine and this folder defines the enforcement details.
```

## Rule files

```text
00-core-rules.md                 Global invariants
01-project-brain-rules.md        Project Brain and freshness
02-onboarding-rules.md           Onboarding boundaries
03-agent-factory-rules.md        Generated coder creation
04-task-analysis-rules.md        Task normalization
05-coder-leader-rules.md         Multi-service coordination
06-service-coder-rules.md        Generated coder behavior
07-dev-verification-rules.md     Code Done gate
08-qc-rules.md                   QC execution
09-bug-routing-rules.md          Blocking and non-blocking bugs
10-memory-rules.md               Durable memory updates
11-approval-gates.md             User approval requirements
12-artifact-contracts.md         Required artifacts and schemas
13-security-secret-rules.md      Secrets, PII, auth-sensitive work
14-skill-composition-rules.md    Skill composition and multi-skill agents
15-model-routing-observability-rules.md  Model profiles, activity dashboard, response UI
16-specialist-advisory-rules.md  Specialist advisors: advisor-only contract, advisory artifacts, invocation
17-hook-enforcement-rules.md     Tool-adapter hooks: scope/secret/destructive guards, profiles
18-doc-precedence-rules.md       Document tier model (T0–T3): one source per decision, higher tier wins
19-autonomous-delivery-rules.md  Autopilot: one-time grant, soft-gate auto-approve, self-heal loop, hard-stops, done = finished product
20-git-workflow-rules.md         Git-flow: branch per task, milestone commits, outward git gated
21-input-prerequisites-rules.md  Required inputs per phase/coder type; refuse on missing/insufficient, coordinator reports the gap
22-artifact-granularity-rules.md Split docs per feature; complete Given/When/Then ACs; full QC test-case coverage (no sketchy/monolithic artifacts)
23-agent-collaboration-rules.md  A2A envelopes: validate handoffs before working; results require evidence; deviations declared
24-purpose-chain-rules.md        Orphan-work gate, intent ledger (journal), claims cite sources
25-working-agreements-rules.md   Echo-back, WIP=1, DoR/DoD, honest status, escalation etiquette
26-change-integrity-rules.md     Read whole unit, trace callers, remove dead code, one code path not two
27-session-continuity-rules.md   Cross-adapter resume/handoff: state authority order, read_next budget, no policy reset
28-challenge-protocol-rules.md   Critical thinking: challenge triggers, steelman+evidence+alternative, stop/flag/note, decision rights, disagree-and-commit, no sycophantic reversal, blind review, pre-mortem
29-craft-standards-rules.md      The Maestro Way: house standards (CS/DS/AS/WS/AG) as the review bar, precedence, craft gates, review records
30-learning-loop-rules.md        Study before build, pre-flight lessons, retro, promotion ladder, prevention over resolution, quality signals
```

R-028..R-030 keep the same ids in every Maestro template so findings and challenges cite one
vocabulary everywhere. House standards referenced by R-029 live in `../standards/` (see
`../standards/README.md`).
