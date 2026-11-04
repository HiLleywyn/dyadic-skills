# Severity and confidence

## Keep the dimensions separate

Severity measures potential impact under supported exploit conditions. Confidence measures how strongly the evidence establishes the finding. Reportability includes additional considerations such as scope, novelty, duplicate status, program rules, and whether the behavior violates a security boundary.

A high-severity hypothesis with weak reachability evidence remains low confidence. A high-confidence low-impact information leak remains low severity. Never inflate one dimension to compensate for another.

## Confidence

### High

Use High when the complete source-to-sink path is established and either safely reproduced or proven through deterministic semantics with all material controls inspected. Preconditions and affected revisions are known. No credible counterevidence defeats the path.

### Medium

Use Medium when the path is strongly supported but a material runtime, deployment, configuration, or external-service condition remains unverified. The missing fact must be named and capable of changing exploitability or scope.

### Low

Use Low for a lead with incomplete reachability, ambiguous attacker control, unknown control effectiveness, uncertain impact, or weak provenance. Low-confidence items stay candidates; they do not enter an external report as established vulnerabilities.

## Severity analysis

Describe severity through explicit questions:

- What privilege and user interaction are required?
- Is the vulnerable component network reachable, tenant-local, or operator-only?
- Does exploitation cross an authentication, authorization, origin, sandbox, cryptographic, confidentiality, integrity, or availability boundary?
- What data, action, value, or service capacity can be affected?
- Is the impact confined to the attacker's own resources?
- How repeatable and scalable is the path under normal controls?
- Which configuration or deployment choices are prerequisites?
- Do rate limits, consent, PKCE, signatures, transaction boundaries, or isolation materially constrain it?

Use qualitative severity when that communicates the evidence more honestly than a score. When a program requires CVSS, select a version and provide the complete vector. Explain each non-obvious metric. Verify the numeric score with a reliable calculator; do not paste a remembered number that does not match the vector.

## Conservative severity guide

- **Critical**  -  reliable compromise with catastrophic confidentiality, integrity, or availability impact across a major trust boundary, ordinarily requiring low privileges and little or no user interaction. Critical is exceptional.
- **High**  -  substantial unauthorized data access, account/control compromise, signing or fund impact, broad code execution, or material secret disclosure with a practical path.
- **Medium**  -  meaningful boundary violation with significant prerequisites, consent, restricted reachability, limited scope, or deployment dependence.
- **Low**  -  limited impact, narrow information exposure, defense-in-depth weakness, or behavior requiring unusually strong attacker position.
- **Informational / hardening**  -  useful improvement without a demonstrated security-boundary violation.

## CWE and taxonomy

Choose the narrowest CWE that describes the product's defect, not merely the attacker's prerequisite. For example, an upstream open redirect may be required to exploit a downstream origin-validation flaw; the downstream report should not automatically be labeled CWE-601. Cite multiple CWEs only when each independently clarifies the root cause.

## Counterevidence

List controls that were tested and found effective, not only those that failed. A control may reduce severity without disproving the finding. If a control fully prevents the claimed impact under supported configurations, mark the candidate DISPROVEN or narrow the claim.
