# Dyadic Security Skills

This collection provides Dyadic-native workflows for defensible security assessment: defining scope, modeling threats, discovering candidates, tracing attack paths, validating findings, writing reports, implementing narrow fixes, verifying remediation, reviewing diffs, proposing hardening, defining repository policy, and tracking accepted findings.

These are operational instructions for Iris. They use Dyadic's existing tool discovery, workspace, isolated execution, approval, and evidence systems; they do not install a scanner, provide credentials, or grant authority to test a target. Runtime tool schemas and the user's current authorization remain authoritative.

## Skills

| Skill | Purpose |
| --- | --- |
| [Security Scan](dyadic-security-scan/SKILL.md) | Single-pass, repository-wide or scoped assessment with an immutable snapshot and coverage receipt |
| [Security Diff Scan](dyadic-security-diff-scan/SKILL.md) | Review a commit, branch, pull request, or patch for vulnerabilities introduced by the change |
| [Threat Model](dyadic-threat-model/SKILL.md) | Identify assets, actors, trust boundaries, abuse cases, assumptions, and prioritized review surfaces |
| [Finding Discovery](dyadic-finding-discovery/SKILL.md) | Generate evidence-linked vulnerability candidates without prematurely reporting them |
| [Attack Path Analysis](dyadic-attack-path-analysis/SKILL.md) | Trace attacker input through transformations and controls to a security-relevant sink and impact |
| [Finding Validation](dyadic-finding-validation/SKILL.md) | Reproduce or disprove candidates, evaluate countercontrols, and issue a reportability verdict |
| [Vulnerability Write-up](dyadic-vulnerability-writeup/SKILL.md) | Produce self-contained disclosure reports with portable proof, history, impact, and remediation |
| [Fix Finding](dyadic-fix-finding/SKILL.md) | Implement a minimal authorized remediation and focused regression coverage |
| [Verify Fix](dyadic-verify-fix/SKILL.md) | Verify a proposed fix against the original exploit path and surrounding behavior |
| [Security Hardening](dyadic-security-hardening/SKILL.md) | Turn observed risk into prioritized architectural defenses without presenting them as vulnerabilities |
| [Security Policy](dyadic-security-policy/SKILL.md) | Create or revise SECURITY.md scope, reporting, safe-harbor, and response guidance |
| [Track Findings](dyadic-track-findings/SKILL.md) | Deduplicate and record validated findings in an approved issue or advisory system |

## Shared standards

- [Dyadic runtime and tool discipline](_shared/runtime-and-tools.md)
- [Authorization and safe testing](_shared/safe-testing.md)
- [Evidence and provenance](_shared/evidence-standard.md)
- [Severity and confidence](_shared/severity-and-confidence.md)
- [Validation rubric](_shared/validation-rubric.md)
- [Disclosure report standard](_shared/report-standard.md)
- [Finding record schema](_shared/finding.schema.json)
- [Synthetic validated finding](examples/validated-finding.json)

These shared files preserve the original authoring collection. The adopted 1.0.1 packages each include the standards they use under their own `references/` and a finding validator under `scripts/`. Install the complete individual folder; sibling `_shared/` paths are no longer required. The package's linked resources are authoritative for that version. Runtime changes belong in Dyadic's source catalog and are mirrored back here with [source hashes](../catalog-source.json).

## Safety and authority

The skill text never expands authorization. Public source review, local parsing, and disposable offline reproduction are different from testing a live service. A connected tool, API key, browser session, vulnerability-disclosure program, or broad user statement does not erase the target's written scope, rate limits, data-handling rules, or prohibited-test conditions. Before an external mutation or live test, identify the exact target, permitted identity, method, expected effect, rollback, budget, and stop condition.

Do not expose secrets, persist customer data, reuse discovered credentials, execute untrusted samples, degrade service, or create a report merely because a static pattern looks dangerous. Preserve negative results and unresolved coverage; they are part of the engineering record.

## Validation

Every skill folder must pass the skill-creator `quick_validate.py` check. The collection additionally validates manifest IDs, versions, frontmatter names, relative links, and finding records with the scripts in `scripts/`. These checks establish package consistency, not the correctness of a security conclusion.

Run `python dyadic/scripts/verify_catalog_mirror.py` from the repository root to check every adopted package against its recorded source hashes. Dyadic's `tools/catalog_check.py` additionally builds the real installed bundles and checks their resource closure. The twelve package validators are byte-identical; validate a synthetic record with one and confirm an invalid record is rejected. No helper runs during installation.
