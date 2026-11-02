# Finding validation rubric

## Promotion gate

A candidate becomes a validated finding only when the evidence answers all applicable questions:

### Attacker control

- Which exact field, message, file, state, identity, or timing can the attacker control?
- At what privilege and tenant boundary?
- Can normal validation, canonicalization, or protocol parsing remove that control?

### Reachability

- What production or supported entry point reaches the vulnerable operation?
- Are feature flags, environment settings, permissions, hardware, or deployment topology required?
- Is the path dead code, test-only, example-only, admin-only, local-only, or legacy-but-shipped?

### Security boundary

- Which documented or structurally evident boundary is crossed?
- Is the observed behavior intentional and disclosed?
- Does the result affect something other than the attacker's own data or process?

### Controls

- Where are authentication, authorization, origin, signature, nonce, replay, rate, size, sandbox, escaping, and transaction controls applied?
- Are they applied to the original value, canonical value, and final destination?
- Do redirects, retries, queues, caches, asynchronous jobs, or alternate serializers bypass them?

### Impact

- What exact unauthorized read, write, execution, disclosure, value movement, or service loss occurs?
- Can the impact be demonstrated with synthetic data and without maximizing harm?
- Which downstream privileges are assumed rather than established?

### Repeatability and versions

- Is the behavior deterministic?
- Which revision was tested?
- Which releases are actually verified affected or fixed?
- Does the proof depend on a race, external provider, or unusual configuration?

## Validation methods

Use the least risky method that can decide the candidate:

1. deterministic source semantics with complete caller and control review;
2. focused existing unit or integration test;
3. added regression test with synthetic fixtures;
4. disposable local service or container with loopback and mocked dependencies;
5. approved staging/testnet probe with a tester-owned identity;
6. low-volume live proof only when explicitly authorized and necessary.

Record negative controls. A convincing proof often demonstrates both the vulnerable behavior and the effectiveness of an adjacent control—for example, a response leaks a synthetic key while the logger redacts it.

## Dispositions

- **validated-reportable** — security boundary and impact are established, scope permits reporting, and the report can be self-contained.
- **validated-nonreportable** — behavior is real but intended, out of scope, duplicate, self-only, or below the program's threshold.
- **needs-evidence** — a specific missing fact could promote or disprove the candidate; name the smallest safe test or document needed.
- **disproven** — a control, unreachable path, invalid assumption, or failed reproduction defeats the claim.
- **hardening-only** — the proposal reduces risk but no present vulnerability is established.

## Independent review

For high-impact, externally submitted, or architecture-dependent findings, obtain an independent skeptical pass when available. Give the reviewer the pinned source and candidate, not the desired conclusion. Ask them to locate counterevidence, alternative interpretations, unsafe proof steps, and severity inflation. Resolve disagreements in the record; do not average them away.

## Required validation output

- disposition and confidence;
- one-sentence root cause;
- affected security boundary;
- exact prerequisites;
- source-to-sink trace;
- reproduction or deterministic proof;
- counterevidence and controls;
- affected/fixed version evidence;
- severity rationale and CWE;
- safe remediation direction;
- limitations and untested conditions.
