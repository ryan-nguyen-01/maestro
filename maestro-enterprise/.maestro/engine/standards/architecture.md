# Architecture Standard (AS)

The house bar for system design: the blueprint's architecture proposal, HLD/LLD, ADRs, and the solution
architect's review. Levels and precedence: [README.md](README.md). Specialist depth comes from the
architecture advisors (api-designer, database-architect, event-architect, cloud-architect) and skills.

## A. Decide from the problem

```text
AS-01 MUST   Every architectural choice cites the acceptance criterion, NFR, or constraint that forces it.
             "Best practice" or "scalable" alone is not a reason.
AS-02 SHOULD Boring by default: proven technology the project (and its coders) already know. Novel tech
             spends one of at most one "innovation token" per project and needs written justification.
AS-03 SHOULD Modular monolith first. Split into separately deployed services only for a concrete forcing
             reason — independent scaling, release cadence, ownership, fault isolation, or a compliance
             boundary — recorded in an ADR.
```

## B. Boundaries and contracts

```text
AS-04 MUST   Each module owns its data. Other modules use its public interface or contract — never its
             tables, internal classes, or private endpoints.
AS-05 MUST   Contracts first: API, event, and schema contracts are written and reviewed before
             implementation; versioned; changed additively by default. A breaking change has a
             deprecation path and a consumer list.
AS-06 SHOULD Boundaries follow ownership: one component, one owning coder; cross-component change goes
             through the coder leader (Conway's law, made explicit).
```

## C. Decisions that survive a challenge

```text
AS-07 MUST   Classify each decision by reversibility.
               One-way door (data model, public API, auth/tenancy model, vendor or cloud lock-in, money
               flows): ADR + >= 2 real alternatives + a pre-mortem (R-028-07) + user visibility.
               Two-way door (library inside a module, internal naming, folder layout): decide quickly,
               one journal line, revisit cheaply.
AS-08 MUST   Alternatives are real: at least two options including the simplest viable one (often
             "extend what exists" or "do nothing yet"), each with why it lost. One option is not a decision.
```

## D. Designed for failure

```text
AS-09 MUST   For every external dependency (database, queue, third-party API, LLM): timeout, retry policy,
             fallback or degradation, and what the user sees when it is down.
AS-10 SHOULD NFRs are numbers with a measurement: p95 latency, throughput, availability, RPO/RTO, data
             volume growth — right-sized to the scope target (MVP keeps them light but explicit).
AS-11 SHOULD Consistency is a stated choice per flow (strong vs eventual) with the user-visible effect of
             eventual consistency handled (read-your-writes, pending states).
AS-12 SHOULD Observability is designed in: correlation ids across boundaries, health endpoints, the three
             or four metrics that say whether each critical flow works.
```

## E. Security and data by design

```text
AS-13 MUST (floor) A threat model (STRIDE-lite is enough) whenever the design touches authentication,
             authorization, payments, PII, multi-tenancy, file upload, or LLM tool use. Least privilege,
             secrets in a manager, TLS everywhere, encryption at rest for sensitive data.
AS-14 SHOULD One source of truth per entity. Derived copies (caches, read models, search indexes) name
             their source and their staleness budget.
AS-15 SHOULD Production-target designs state the order-of-magnitude running cost and its main driver.
```

## F. Communicate the design

```text
AS-16 MUST   Diagrams as code (Mermaid) at C4 levels 1-2 (context, containers) in the HLD, plus a sequence
             diagram for each critical flow. Diagrams change in the same change as the design.
AS-17 SHOULD An LLD per feature names the files/modules touched, the contracts, the data changes, the error
             cases, and the test approach — enough that a coder never has to guess (R-021).
```

## Architecture review checklist

```text
[ ] Each choice traces to an AC/NFR/constraint (AS-01)
[ ] Simplest viable option considered and honestly compared (AS-03, AS-08)
[ ] One-way doors identified, each with ADR + alternatives + pre-mortem (AS-07)
[ ] Boundaries own their data; contracts written and versioned (AS-04/05)
[ ] Every dependency has timeout / retry / fallback / user-visible behavior (AS-09)
[ ] NFRs are numbers; consistency model stated per flow (AS-10/11)
[ ] Threat model done where the floor requires it (AS-13)
[ ] Diagrams current (AS-16); LLD sufficient for coders (AS-17)
```
