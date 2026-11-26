# R-029: Craft Standards (The Maestro Way)

## Applies to

Every agent that produces or reviews an artifact: coders and Coder Leader (code), UI/UX designer and
accessibility auditor (design), Solution Architect and architecture advisors (architecture), every
author (documents), agent builders and the eval engineer (AI agents), Dev Verification and QC (gates).

## Purpose

Process rules make sure the right steps happen. Craft standards make sure what each step produces is
good — by one explicit, recognizable house bar instead of whatever style each run happens to choose.
Standards live in `.maestro/engine/standards/`: `code.md` (CS), `design.md` (DS), `architecture.md`
(AS), `writing.md` (WS), `agents.md` (AG), with levels and precedence in `README.md`.

## Rules

```text
R-029-01: APPLY BY DEFAULT. A producing agent applies the standards for its output type while it works,
  not after review. Before writing in a technology that has a matching skill, load that skill: the
  standard sets the floor, the skill sets the idiom (R-014).
R-029-02: PRECEDENCE. MUST (floor) items > approved project decisions (blueprint, ADR, contracts, ACs)
  > project conventions and established codebase patterns > house MUST/SHOULD > taste. In an existing
  codebase, consistency with its patterns beats the house default; record each deviation once in
  .maestro/knowledge/conventions.md. Floor items never bend without an explicit, recorded user
  decision for that specific case, and never for secrets or data loss.
R-029-03: FINDINGS CITE IDS. Every review finding is written as
  [<ID>][<LEVEL>] <location> — <problem>. Fix: <concrete fix>.
  MUST = blocker; SHOULD = needs a disposition (fixed, or one line of justification); MAY never blocks.
  A finding with no standard id behind it is taste (R-025-08) and cannot block.
R-029-04: CRAFT GATES.
    Direction gate     architecture proposal against AS-01..09; UI prototype against design.md
                       (design review checklist) BEFORE it is shown to the user for approval
    Architecture review AS checklist; pre-mortem for one-way doors (R-028-07)
    Design → UI code   no UI code before the prototype passed design review and was approved (DS-21)
    Code review        Coder Leader reviews against code.md in the review order (R-005-09)
    QC                 re-check DS-04, 06, 07, 13-18 on the built UI; failures are bugs
    Agents (AI)        agents.md checklist and the eval gate before an agent is called done
R-029-05: RECORD THE REVIEW. Governed and autonomous work writes one craft review per gate to
  .maestro/work/tasks/<task-id>/reviews/<gate>-<seq>.yaml from craft-review.template.yaml, performed in
  a fresh context (R-028-06). Dev Verification runs the CRAFT-REVIEW critical check: Code Done is
  rejected when the code review record is missing, was not independent, or has an open MUST finding.
R-029-06: PROPORTIONALITY. direct: the author self-checks MUST items touched by the change and notes it
  in the journal line. assisted: self-check + role-owner review, findings in the journal. governed /
  autonomous: full craft review records with an independent reviewer. Risk escalation raises the level.
R-029-07: HOUSE DIRECTION. A UI product with no brand or design system starts from the house token
  baseline in design.md and adapts it at the Direction gate; the chosen direction is recorded in
  product-blueprint.yaml ui_ux. Generic, unstyled, or lorem-ipsum prototypes are not presented.
R-029-08: STANDARDS ARE STABLE INSIDE A WORKSPACE. Agents do not edit .maestro/engine/standards/ in an
  applied workspace (R-025-11). Project-specific rules go to conventions.md as PC-<n> entries, and
  generalizable lessons become standard proposals through the learning loop (R-030).
```

## Violation handling

A result that ignores a MUST is returned with the finding. A gate passed without its review record
(governed/autonomous) is invalid and re-opened by Workflow Policy. Recurring findings of the same id
feed the learning loop (R-030) as anti-patterns.
