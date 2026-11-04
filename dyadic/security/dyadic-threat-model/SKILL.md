---
name: dyadic-threat-model
description: Create or update an evidence-backed threat model for a repository, service, protocol, feature, or architecture in Dyadic. Use when security review needs assets, actors, trust boundaries, data flows, abuse cases, assumptions, and prioritized controls; do not use to claim a vulnerability without a demonstrated attack path.
---

# Dyadic Threat Model

Produce a living security model that directs engineering and review effort. The model describes what must be protected, from whom, across which boundaries, under which assumptions. It is not a generic checklist and not a vulnerability report.

Read [runtime and tools](references/runtime-and-tools.md), [safe testing](references/safe-testing.md), and [evidence and provenance](references/evidence-standard.md).

## Define the modeled system

State the system, revision or architecture version, deployment environments, included components, excluded dependencies, user populations, and intended security properties. Read architecture, deployment, authentication, data-model, API, queue, plugin, and operational documentation, then verify important claims against source or configuration.

If the system is too broad, decompose it by trust boundary rather than arbitrary directory: identity, control plane, data plane, execution plane, extension/plugin plane, client/native bridge, billing/quotas, release pipeline, and observability.

## Identify assets and invariants

Name concrete assets and the invariant each requires. Examples:

- session tokens must be usable only by the intended account and origin;
- tenant objects must never be readable or mutable across tenant scope;
- signing keys must not enter logs, responses, prompts, or untrusted workers;
- approval-required tools must not execute before a valid approval bound to the exact request;
- queued work must preserve actor, tenant, policy, and idempotency context;
- provider quota and spend must remain attributable and bounded;
- published artifacts must correspond to the reviewed revision;
- contract messages must be authentic, replay-safe, and domain-separated.

Avoid vague assets such as “the database.” Name the data and unauthorized effect that matters.

## Enumerate actors and capabilities

Include anonymous clients, ordinary users, organization members, owners, administrators, support staff, external providers, compromised dependencies, malicious content authors, plugin authors, CI identities, background workers, network peers, and insiders where relevant. Distinguish what each actor legitimately controls: headers, object IDs, files, redirects, prompts, package manifests, timing, provider responses, signatures, or deployment settings.

Do not assume every actor starts on the Internet. Local operators, authenticated tenants, browser origins, peer nodes, compromised workers, and supply-chain contributors occupy different positions.

## Draw data flows and trust boundaries

For each important flow, record source, authentication, authorization context, transformation, storage, transport, sink, response, and audit trail. Mark boundaries where identity or policy can be lost:

- proxy to application;
- browser to API;
- API to queue and worker;
- tenant workspace to sandbox;
- model to tool broker;
- plugin to host;
- application to provider;
- source repository to CI and release;
- chain/domain to bridge verifier;
- public content to renderer or crawler.

A small text or Mermaid diagram is useful when it clarifies three or more relationships. Keep the accompanying table authoritative so the model remains accessible without rendering.

## Generate abuse cases

Use architecture-specific abuse stories, not a rote STRIDE list. For each story include actor, starting capability, sequence, broken invariant, expected control, impact, and evidence that would confirm or reject it. Cover control-plane misuse, alternate serializers, redirects, stale caches, retries, partial failure, concurrency, fallback behavior, size/cost exhaustion, and administrative support paths.

Prioritize by plausible attacker position, asset value, boundary complexity, control maturity, and ease of safe validation. Explicitly include abuse cases that would remain important even if the most dramatic hypothesis is false.

## Map controls and gaps

For every high-priority abuse case, identify preventive, detective, and recovery controls. Record whether the control is source-confirmed, documented-only, deployment-dependent, or absent. A missing defense is a hardening gap until a reachable impact is demonstrated.

Controls to inspect include canonicalization, object ownership, scope binding, cryptographic verification, nonce/replay state, transaction boundaries, output encoding, sandboxing, egress policy, rate and cost budgets, audit logging, key rotation, feature defaults, and release attestation.

## Deliverable

Produce:

1. scope and immutable architecture identity;
2. assets and invariants;
3. actor/capability table;
4. trust boundaries and data flows;
5. ranked abuse cases;
6. control matrix with evidence state;
7. assumptions and unresolved dependencies;
8. prioritized review plan naming the smallest evidence needed next.

Update an existing model without erasing prior assumptions or decisions; mark what changed and why. Route concrete candidates to `$dyadic-finding-discovery` or `$dyadic-attack-path-analysis` rather than declaring them vulnerabilities in the threat model.

## Installed Resources

Use `tools.load(inventory=true)` to discover enabled skills and permitted tools. Load the skills group,
then read this package with `skills.read(name="dyadic-threat-model", path="SKILL.md")`.
Read linked references using the same skill name and their bundle-relative paths. Cross-skill `$name`
references describe optional workflows, not callable tool names; discover an enabled sibling first.
If it is unavailable, perform the supported part directly and record the remaining phase as unexecuted.

For a durable record, use the [finding schema](references/finding.schema.json). The bundled
[validator](scripts/validate_finding.py) checks record invariants without third-party packages; it does
not establish that a finding is true. Run it only through an authorized execution tool.
