# Evidence and provenance standard

## Consequential claim states

Classify each material claim. Do not collapse these labels into a single confidence score.

- **CONFIRMED**  -  directly demonstrated by a reliable primary record or reproducible execution against the pinned artifact.
- **CORROBORATED**  -  supported by multiple independent credible sources or independent validation paths.
- **INFERRED**  -  a reasoned interpretation whose assumptions are stated and whose alternatives remain possible.
- **UNRESOLVED**  -  evidence is missing, inaccessible, contradictory, or outside permitted testing.
- **DISPROVEN**  -  the tested hypothesis is contradicted by reliable evidence at the assessed revision and configuration.

“No finding” means no reportable issue survived the described coverage. It never means the target is safe.

## Evidence record

Every candidate or finding should be reconstructable from records containing:

- stable finding or candidate ID;
- target and immutable revision or artifact digest;
- source path and verified one-based line number, symbol, endpoint, selector, or transaction identifier;
- exact observation, not a conclusion disguised as evidence;
- collection method and timestamp;
- execution environment and authorization tier;
- supporting artifact digest when a file is retained;
- counterevidence and evaluated controls;
- assumptions, limitations, and unreviewed surfaces;
- claim state and confidence;
- relationship to earlier occurrences or duplicates.

When a webpage or API response is relevant, preserve the canonical URL, retrieval time, response status when available, and a short attributable excerpt. Do not quote more than needed. Screenshots are supplementary; retain the machine-readable response or source whenever possible.

## Source-to-sink trace

A vulnerability trace should identify:

1. attacker-controlled source;
2. parser and normalization steps;
3. authentication and authorization context;
4. state transitions and storage;
5. guards, sanitizers, allowlists, rate limits, and policy checks;
6. security-relevant sink;
7. returned or externally observable effect;
8. concrete impact and required privileges;
9. countercontrols that reduce or prevent exploitation.

Quote only the smallest code fragments needed to make the trace independently understandable. Record the full paths and lines privately; portable reports use repository-relative paths.

## Coverage receipt

Every completed assessment must name:

- fully reviewed files or components;
- mechanically searched patterns and their purpose;
- tests, builds, analyzers, and runtime probes actually executed;
- important paths sampled but not exhaustively reviewed;
- paths excluded by scope, size, generated/vendor status, missing dependencies, or unavailable hardware;
- configuration and deployment assumptions;
- external services and live environments not tested;
- unresolved candidates and why they were not promoted.

Coverage receipts prevent a polished report from implying broader assurance than the work supports.

## History and version evidence

For a validated source finding, establish when practical:

- introducing commit and date;
- intent visible in commit message, change request, or test;
- earliest verified affected release;
- current affected release or upstream revision;
- fixed commit and first verified fixed release, if any;
- whether backports or divergent branches change the result.

Do not claim “all versions” from one current snapshot. If exact package-to-commit mapping is unavailable, state the earliest and latest versions actually verified.

## Secrets and personal data

Replace secrets with deterministic placeholders before storing commands, logs, reports, or screenshots. A hash of a secret is still sensitive when the input space is small. Do not retain raw customer records. Describe the minimum observed schema or synthetic proof instead.

## Artifact integrity

Hash retained artifacts when the digest helps prove consistency. A digest proves that two byte sequences match; it does not prove provenance, safety, authorship, or truth. Store original evidence read-only and create derived analysis separately. Preserve amendments rather than silently overwriting earlier conclusions.
