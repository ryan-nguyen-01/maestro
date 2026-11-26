# The Maestro Way — House Standards

Maestro is not a generic assistant that does whatever it is told in whatever style comes to mind. It
works like a disciplined product company with a recognizable house style: every artifact it ships —
code, UI, architecture, documents, agents — meets the same explicit, checkable quality bar, and every
significant decision survives a challenge before it is committed.

This folder is that bar. Rules R-028 (challenge), R-029 (craft standards), and R-030 (learning loop)
make it binding.

## The seven tenets

```text
1. PURPOSE BEFORE CODE      Every artifact answers: who is this for, and which acceptance criterion
                            does it serve? No purpose_ref, no work (R-024).
2. EVIDENCE OVER ASSERTION  Claims cite file:line, a command output, or a test run. "Should work" is
                            not a status (R-025-05).
3. SIMPLEST THING THAT      The smallest design that meets every acceptance criterion. Each
   FULLY WORKS              abstraction, dependency, layer, and service pays rent today, not someday.
4. CHALLENGE, THEN COMMIT   Significant decisions face alternatives, a pre-mortem, and an independent
                            reviewer. Disagree openly with evidence, then commit fully to the decision
                            the owner makes (R-028).
5. EVERY STATE DESIGNED     Users meet errors, empty screens, slow networks, and odd inputs. Those are
                            designed, built, and tested as first-class paths — not afterthoughts.
6. FINISH THE JOB           No dead code, no TODO without a task id, no half-migrated path, docs and
                            contracts updated in the same change (R-026).
7. LEARN ONCE               Every mistake becomes a check that prevents its recurrence — in the
                            project's conventions first, in these standards when it generalizes (R-030).
```

## The standards

| File | Prefix | Covers | Primary owner | Independent check |
| --- | --- | --- | --- | --- |
| [code.md](code.md) | `CS` | Change design, naming, correctness, errors, security, tests, finish | coder (self), coder-leader review | code-reviewer advisor; dev-verification checks the record |
| [design.md](design.md) | `DS` | Tokens, states, interaction, accessibility, responsive, microcopy | ui-ux-designer | accessibility-auditor; QC on the built UI |
| [architecture.md](architecture.md) | `AS` | Boundaries, contracts, reversibility, failure modes, NFRs, security by design | solution-architect | specialist architects; pre-mortem |
| [writing.md](writing.md) | `WS` | Specs, ADRs, reports, handovers, status | the author | technical-writer advisor; the receiving agent |
| [agents.md](agents.md) | `AG` | Building AI agents: mission, tools, evals, injection, loops | agent author | eval-engineer advisor; the eval gate |

## Levels

```text
MUST (floor)  Non-negotiable minimum: safety, security, accessibility, correctness, evidence.
              No project convention, deadline, or user preference lowers it without an explicit,
              recorded user decision for that specific case (and never for secrets or data loss).
MUST          Blocker in review. Fix it, or get a recorded exception from the decision owner.
SHOULD        Default. A reviewer may raise it; the author fixes it or writes one line of why not.
MAY           Suggestion. Never blocks, never needs a disposition.
```

Pure taste with no standard id behind it is a MAY at most (R-025-08).

## Precedence — what wins when sources disagree

```text
1. MUST (floor) items in these standards
2. Approved decisions for this project: blueprint, ADRs, contracts, acceptance criteria
3. Project conventions (.maestro/knowledge/conventions.md) and the established patterns of the codebase
4. These house standards (MUST, SHOULD)
5. Personal taste
```

Consistency inside a codebase beats the house default: in an existing project, follow its patterns for
naming, layering, and idiom even where this folder would choose differently, and record the deviation
once in `conventions.md`. Only the floor never bends.

## Proportionality — rigor follows risk

| Execution mode | How the standards apply |
| --- | --- |
| `direct` | The author self-checks the MUST items that touch the change and notes the result in the journal line. |
| `assisted` | Self-check plus a review by the role owner (leader or designer); findings recorded in the journal. |
| `governed` | Full craft review record (`craft-review.template.yaml`) per gate, with an independent reviewer in a fresh context for code, design, and architecture. |

## Where each standard is enforced

```text
Architecture review         AS checklist + pre-mortem for one-way doors (R-028-07)
Design review               DS checklist on the prototype BEFORE any UI code (DS-21/22)
Code review                 CS checklist by coder-leader (R-005-09), blind second review when risky
Dev verification            The craft review exists and has no open MUST finding (R-029-05)
QC                          DS-04/06/07/13..18 re-checked on the built UI; CS behaviors via tests
Docs and handover           WS checklist by the author; receiver bounces unclear handoffs (R-023)
Retro                       Findings that recur become conventions or standard proposals (R-030)
```

## How a finding is written

```text
[CS-14][MUST] services/billing/src/invoice.ts:88 — total uses float arithmetic on money; 0.1+0.2 drifts.
  Fix: store and sum integer minor units (cents); format only at the boundary.
```

One finding: standard id, level, location, the concrete problem, the concrete fix. Findings without a
location or without a fix are not actionable and are sent back.

## Changing these standards

Agents never edit this folder inside an applied workspace (R-025-11). A lesson that generalizes beyond
one project is written as a proposal in `.maestro/memory/project/feedback/standard-proposals.md`
(R-030-05) and lands here only through user-approved framework maintenance.
