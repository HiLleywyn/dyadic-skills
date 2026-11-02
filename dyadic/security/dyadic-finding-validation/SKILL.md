---
name: dyadic-finding-validation
description: Skeptically validate or disprove supplied security candidates against a pinned artifact using source review, counterevidence, and the safest sufficient reproduction. Use before reporting, severity assignment, fixing, or issue creation; do not use to generate a broad new candidate list.
---

# Dyadic Finding Validation

Make a reportability decision that survives skeptical review. Validation is not an exercise in making the candidate work; it is an attempt to identify the exact conditions under which it is true or false.

Read [validation rubric](../_shared/validation-rubric.md), [safe testing](../_shared/safe-testing.md), [evidence and provenance](../_shared/evidence-standard.md), and [severity and confidence](../_shared/severity-and-confidence.md).

## Intake and independence

Retain the candidate's original wording, ID, evidence, and snapshot. Restate the hypothesis without adding impact. Identify what evidence came from the discoverer and what will be independently checked.

When a candidate depends on a complex flow, use or reproduce `$dyadic-attack-path-analysis`. Verify every cited path and one-based line against the pinned revision. Inspect repository policy and scope before runtime work.

## Build the decision matrix

List the minimum facts required for exploitation:

- attacker control and privilege;
- supported entry-point reachability;
- relevant configuration or feature flag;
- control failure;
- sink behavior;
- externally observable unauthorized effect;
- affected version;
- safe proof environment.

For each fact, record supporting evidence, counterevidence, and state: confirmed, contradicted, or unverified. Name the single missing fact most likely to change the verdict.

## Reproduce safely

Choose the least risky sufficient method from deterministic source semantics, existing tests, a focused regression test, a disposable local service, approved staging/testnet, or an explicitly authorized low-volume live probe.

A good reproduction includes:

- synthetic identity/data/secret;
- exact setup and dependencies;
- one request or minimal sequence;
- assertion for the unauthorized effect;
- negative control proving the test is not merely observing expected behavior;
- cleanup and retained artifact list;
- known differences from production.

Use mocks for providers, clocks, DNS, queues, and external services when they preserve the deciding semantics. Verify the mock was consumed. If mocking removes the disputed behavior, the test is not sufficient.

## Try to disprove it

Before promotion, explicitly examine:

- global middleware and framework defaults;
- alternative parsers and canonical forms;
- final-destination checks after redirects;
- database constraints and transaction rollback;
- cache keys and invalidation;
- queue/worker actor and tenant context;
- user consent, PKCE, scopes, signatures, nonces, and replay state;
- deployment reachability and network isolation;
- intended operator/admin capabilities;
- output redaction or encoding at the final response;
- tests that demonstrate a safe invariant.

If a control narrows but does not eliminate the path, incorporate it into prerequisites and severity. If it eliminates the claimed impact, mark the candidate disproven or restate a narrower candidate and validate that separately.

## Establish history and affected range

Use Git history, release notes, manifests, tags, and package changelogs to identify introduction and current status. Verify release mappings; do not infer all releases from commit ancestry alone. Search for fixes, reverts, backports, and divergent maintained branches.

If the current revision is the only verified version, say so. Do not delay an otherwise useful report solely because the exact earliest version is unavailable; preserve the limitation.

## Decide severity and taxonomy

Choose confidence first, then severity. Explain attacker position, interaction, boundary, concrete impact, scope, and deployment dependence. Use a CWE that describes the target defect. Calculate CVSS only when requested or required and verify the vector/score pairing.

## Verdict

Return exactly one primary disposition from the shared rubric:

- `validated-reportable`
- `validated-nonreportable`
- `needs-evidence`
- `disproven`
- `hardening-only`

The validation record includes confidence, severity, root cause, numbered attack path, prerequisites, evidence, counterevidence, reproduction receipt, affected/fixed versions, CWE, remediation direction, limitations, and next action. Use the shared JSON schema for durable records.

No external report, issue, disclosure, source patch, or deployment occurs during validation unless the user separately requested that action.
