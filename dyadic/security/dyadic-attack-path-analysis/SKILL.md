---
name: dyadic-attack-path-analysis
description: Trace a supplied security candidate from attacker-controlled source through parsing, identity, policy, state, and controls to a security-sensitive sink and impact. Use when reachability or exploit conditions are unclear; do not use for broad candidate discovery, final report prose, or live exploitation beyond the authorized validation boundary.
---

# Dyadic Attack Path Analysis

Decide whether a candidate has a complete, supported attack path. Produce a structured trace that a validator can reproduce or disprove.

Read [runtime and tools](../_shared/runtime-and-tools.md), [evidence and provenance](../_shared/evidence-standard.md), [safe testing](../_shared/safe-testing.md), and [validation rubric](../_shared/validation-rubric.md).

## Normalize the candidate

Write the hypothesis as:

> An actor with **capability** can supply **source**, which reaches **operation** despite **expected control**, causing **unauthorized impact** to **asset/principal** under **preconditions**.

If any field is unknown, mark it as the analysis question. Pin the source snapshot and retain the original candidate ID. Do not silently strengthen the claim while tracing it.

## Trace the source

Identify the exact attacker-controlled bytes or state and how they enter:

- request body, query, header, cookie, URL, redirect, upload, archive member, protocol message, contract calldata, queue event, provider response, repository content, model output, or timing;
- authentication state, role, tenant, origin, network position, and feature configuration;
- parser type, accepted grammar, duplicate/ambiguous field handling, decoding, normalization, canonicalization, and size limit.

Confirm control through the supported entry point. A value in a unit test helper or internal constructor is not automatically attacker-controlled.

## Follow transformations and state

Enumerate each relevant step with repository-relative path, line/symbol, input shape, output shape, and control:

1. route/protocol dispatch;
2. authentication and identity construction;
3. authorization and policy selection;
4. normalization, redirects, aliases, fallbacks, or version conversion;
5. persistence, cache, queue, retry, or transaction;
6. privileged or externally observable sink;
7. response, callback, artifact, event, or side effect.

Track values, identity, and policy separately. Many defects preserve the data but lose the actor or scope when crossing a queue, cache, serializer, or redirect. For asynchronous paths, record enqueue and consume code and whether authorization is rechecked.

## Inspect controls in the right representation

For each guard, ask which representation it validates and whether the sink uses the same one:

- raw versus decoded path;
- original versus canonical hostname;
- requested versus final redirect URI;
- client-supplied versus database-loaded object;
- pre-migration versus post-migration schema;
- visible field versus derived or fallback field;
- signed bytes versus parsed semantic object;
- request identity versus worker identity;
- pre-cache permission versus cached response consumer.

Inspect deny paths and exception behavior. Fail-open defaults, retries, catch-and-continue blocks, timeout handling, and partial commits may create the boundary failure even when the main path is correct.

## Establish the sink and impact

Name the exact sink: database mutation, file read/write, process spawn, HTML execution, outbound request, credential response, token issue, approval execution, signature acceptance, fund transfer, quota consumption, or service-resource allocation. Show the externally observable effect and which asset or principal is affected.

Do not skip from “dangerous sink” to “RCE” or from “key disclosed” to “account takeover.” Downstream privileges must be independently supported. Keep self-only behavior and intended operator capabilities separate from unauthorized impact.

## Search for alternate paths and controls

Actively try to disprove the candidate:

- Is the entry point disabled or unreachable in supported builds?
- Does an earlier middleware apply globally?
- Does framework output encoding occur after the suspicious code?
- Does the final connector pin a validated address?
- Does the database enforce ownership or uniqueness?
- Does a transaction rollback the apparent partial state?
- Does PKCE, consent, a signature threshold, or nonce prevent the claimed exploit?
- Is the code example-only, test-only, deprecated, or local-admin-only?
- Does the same value become redacted before leaving the process?

Inspect sibling routes and versions both for bypasses and for examples of the intended control.

## Output

Produce:

- normalized hypothesis;
- prerequisites and attacker position;
- numbered source-to-sink trace with evidence;
- control matrix: present, absent, misplaced, bypassed, or unverified;
- concrete boundary and impact;
- alternate paths and counterevidence;
- safe reproduction design;
- remaining deciding questions;
- provisional disposition: complete, incomplete, or disproven.

Do not assign final reportability or severity unless the user specifically asks for combined analysis; hand the trace to `$dyadic-finding-validation`.
