---
name: dyadic-security-hardening
description: Develop prioritized architectural and operational security hardening from validated findings, incidents, threat models, or assessment evidence. Use for defense-in-depth and systemic risk reduction; do not present absent best practices as confirmed vulnerabilities or implement broad changes without an explicit build request.
---

# Dyadic Security Hardening

Translate observed risk into a practical defense roadmap. Preserve the difference between required remediation for a demonstrated vulnerability and defense in depth that reduces likelihood, blast radius, or detection time.

Read [evidence and provenance](../_shared/evidence-standard.md), [severity and confidence](../_shared/severity-and-confidence.md), and [safe testing](../_shared/safe-testing.md).

## Evidence basis

Start from one or more concrete inputs: validated findings, disproven candidates that exposed architectural fragility, incident records, threat models, security policies, deployment diagrams, or control inventories. Pin the source revision or architecture version.

For each proposal, identify:

- observed risk or abuse case;
- asset and trust boundary;
- existing controls and failure mode;
- proposed preventive, detective, or recovery control;
- expected risk reduction;
- compatibility, migration, performance, cost, and operational tradeoffs;
- verification and rollback plan;
- owner and dependency when known.

Do not create a vulnerability count from hardening suggestions.

## Structural priorities

Prefer controls that remove classes of error:

- centralized object/tenant authorization at data access;
- typed identity and policy context preserved across queues and tools;
- canonical final-destination validation for redirects and egress;
- generic external errors plus centralized recursive secret redaction;
- capability-based plugin/agent/tool execution with explicit approval binding;
- network-isolated sandboxes with minimal mounts and controlled egress;
- parameterized interpreters and contextual output encoding;
- cryptographic domain separation, replay-safe nonces, and atomic state transitions;
- default-deny network and service-to-service authentication;
- immutable release provenance, least-privilege CI, and protected signing;
- per-request and aggregate time, memory, collection, output, concurrency, and spend budgets;
- auditable key lifecycle, rotation, revocation, and use attribution.

Avoid brittle payload blacklists, duplicated ad hoc checks, logging raw request objects, or documentation-only controls where enforcement is possible.

## Prioritization

Score proposals qualitatively by:

- risk reduced and number of attack paths covered;
- evidence strength;
- exploit likelihood and exposure;
- implementation complexity and migration risk;
- operational burden and observability;
- dependency on external teams or providers;
- reversibility and ability to verify.

Classify:

- **P0 containment** — immediate action for active compromise or exposed secret; narrowly scoped and reversible;
- **P1 required remediation** — closes a validated high/critical boundary;
- **P2 systemic hardening** — removes recurring classes or materially limits blast radius;
- **P3 hygiene** — useful incremental improvement with modest risk reduction.

Do not label a general best practice P0 merely because it is absent.

## Roadmap design

Sequence work so that containment does not become the permanent architecture. Define milestones with observable acceptance criteria:

- code/config change;
- migration or rollout strategy;
- focused security regression;
- component regression;
- monitoring signal and alert threshold;
- rollback trigger;
- release and deployment identity check;
- documentation and ownership update.

Where a hardening control could break legitimate traffic, propose staged enforcement, telemetry, and a time-bounded compatibility period. Avoid indefinite “testing mode” for security policies without an exit criterion.

## Deliverable

Produce an evidence-to-control matrix, prioritized roadmap, implementation sketches, verification plan, residual risk, and explicit separation among validated remediation, systemic hardening, and hygiene. Do not modify source or infrastructure unless the user separately asks to implement named items.
