---
name: dyadic-finding-discovery
description: Discover plausible security findings in a pinned repository or component and record source-linked candidates for later validation. Use during the candidate-generation phase of an authorized assessment; do not use it to publish unvalidated scanner matches, assign final severity, or perform uncontrolled live exploitation.
---

# Dyadic Finding Discovery

Generate a small set of high-value, evidence-linked candidates. Optimize for attack paths that can be independently decided, not for the number of warnings.

Read [runtime and tools](references/runtime-and-tools.md), [safe testing](references/safe-testing.md), [evidence and provenance](references/evidence-standard.md), and the target's threat model when one exists.

## Inputs

Require an immutable target snapshot, scope, architecture context, and authorization boundary. If invoked inside a scan, reuse its target record rather than creating a second inconsistent identity. Read repository instructions and security policy first.

Build a concise inventory of entry points, identities, object scopes, privileged operations, parsers, egress, execution, storage, and limits. Rank surfaces by attacker control and asset impact.

## Discovery strategy

Use multiple complementary passes:

### Entry-point pass

Start at routes, RPC handlers, protocol messages, upload/import paths, webhooks, callbacks, native intents, CLI arguments, queue consumers, plugin hooks, and public contract functions. Trace authentication, validation, and object scope before following the request into state or sinks.

### Sink pass

Search for command execution, dynamic evaluation, filesystem access, archive extraction, database queries, raw HTML, redirects, outbound requests, deserialization, cryptographic acceptance, secret serialization, privileged mutations, and unbounded work. Trace backward to every reachable caller.

### Invariant pass

Search for inconsistent enforcement of tenant ownership, role, scope, origin, nonce, signature, approval, transaction, output encoding, or size/cost limits across parallel routes and serializers. Compare create/read/update/delete, sync/async, REST/GraphQL/RPC, browser/native, v1/v2, normal/admin, and primary/fallback implementations.

### Historical pass

Inspect security-relevant commits, reverts, TODOs, disabled tests, migration shims, “temporary” compatibility behavior, and architectural redesigns. History can explain intent and identify dormant seams, but an old discussion is not proof that current code is vulnerable.

### Mechanical pass

Use targeted searches or static analyzers for language-appropriate dangerous APIs and missing limits. Triage each result in context. Preserve query purpose and result count in the coverage receipt; do not paste thousands of raw matches into the candidate set.

## Candidate gate

Create a candidate only when all four statements can be written:

1. attacker controls or materially influences a specific source;
2. a supported/reachable path carries it toward a security-sensitive operation;
3. a named control appears absent, misplaced, inconsistent, or bypassable;
4. exploitation could cross a concrete boundary or affect another principal/resource.

Each candidate record includes stable ID, title, target revision, source/sink trace, suspected CWE, prerequisites, impact hypothesis, strongest evidence, strongest counterevidence, confidence, and the smallest safe validation step.

## High-value review prompts

- Is policy checked on an original URL but not the final redirected destination?
- Does a serializer, log, exception, telemetry event, or debug response include secrets or personal data?
- Does a stored-object or alternate route bypass middleware applied to the primary route?
- Does a background job reconstruct actor or tenant context incorrectly?
- Can a retry, cancellation, or partial failure consume a nonce or commit half a transaction?
- Are collections, archives, recursion, output, execution time, concurrency, or provider spend bounded per request and in aggregate?
- Does a parser accept more syntax than the validator reasons about?
- Does a cache key omit identity, scope, locale, permission, or feature state?
- Do plugin, agent, model, MCP, or tool instructions cross an approval or sandbox boundary?
- Can an attacker influence a release artifact, dependency source, workflow token, or signing step?

These prompts guide review; they are not findings.

## Stop and handoff

Stop expanding a candidate once the deciding evidence is clear. Send candidates to `$dyadic-attack-path-analysis` when the flow is complex and to `$dyadic-finding-validation` for a verdict. Preserve rejected candidates with a short reason so future passes do not rediscover the same false positive.

Discovery output must not contain final external-report language, unsupported affected-version ranges, or severity claims beyond a provisional priority. Do not create issues or notify maintainers during discovery.

## Installed Resources

Use `tools.load(inventory=true)` to discover enabled skills and permitted tools. Load the skills group,
then read this package with `skills.read(name="dyadic-finding-discovery", path="SKILL.md")`.
Read linked references using the same skill name and their bundle-relative paths. Cross-skill `$name`
references describe optional workflows, not callable tool names; discover an enabled sibling first.
If it is unavailable, perform the supported part directly and record the remaining phase as unexecuted.

For a durable record, use the [finding schema](references/finding.schema.json). The bundled
[validator](scripts/validate_finding.py) checks record invariants without third-party packages; it does
not establish that a finding is true. Run it only through an authorized execution tool.
