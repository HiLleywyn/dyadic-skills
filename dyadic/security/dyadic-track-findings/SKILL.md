---
name: dyadic-track-findings
description: Deduplicate and record validated security findings in an approved issue tracker, advisory system, or private project with evidence, status, ownership, and remediation state. Use when the user asks to persist or update findings; do not create external tickets from unvalidated candidates or expose private vulnerability details in a public project.
---

# Dyadic Track Findings

Maintain a durable, auditable finding lifecycle without duplicating reports or leaking sensitive evidence. Tracking is an external mutation: prepare the record, show the intended changes, and use the destination's approval flow.

Read [evidence and provenance](../_shared/evidence-standard.md), [severity and confidence](../_shared/severity-and-confidence.md), [report standard](../_shared/report-standard.md), and the destination's visibility/access model.

## Intake gate

Accept validated reportable findings, accepted nonreportable engineering risks, hardening items explicitly requested for tracking, or fix-verification updates. Candidates with `needs-evidence` remain in the private assessment record unless the user wants a research task—not a vulnerability ticket.

Confirm:

- destination repository/project and visibility;
- whether the record should be a private issue, draft advisory, vulnerability report, or internal task;
- target revision and finding ID;
- sensitivity of proof, affected versions, and exploit details;
- required labels, owners, milestones, and disclosure embargo;
- authority to create or update the record.

Never put an unpatched exploit, secret, customer data, or private report in a public issue.

## Deduplicate

Search existing open and closed records using root cause, affected component, sink, CVE/CWE, paths, finding IDs, and alternate titles. Compare semantics, not only wording. A candidate is duplicate when the same root cause and remediation boundary cover it; similar impact in a different control path may require a separate record.

If a duplicate exists, prepare an update or link rather than creating another issue. Preserve distinct occurrences when they affect different maintained branches or products and require separate remediation.

## Canonical record

Track:

- stable finding ID and concise title;
- target, component, revision, affected/fixed versions;
- status and claim state;
- severity, confidence, CWE, and CVSS vector if required;
- root cause and boundary;
- prerequisites and impact;
- private evidence/report link or sanitized summary;
- remediation acceptance criteria;
- owner, priority, milestone, and dates;
- duplicate and related-finding links;
- fix commit/release/deployment identities as separate fields;
- verification verdict and residual risk;
- disclosure/credit state.

Recommended lifecycle:

`candidate-private → validated → accepted → fixing → fix-proposed → verified-source → released → verified-deployed → disclosed/closed`

Use only states supported by the destination and map them explicitly. Do not mark `fixed` because a patch exists; source verification, release publication, and deployment are separate facts.

## Create or update

Prepare the exact title, body, metadata, and visibility before invoking a mutation. Use one canonical issue/advisory per finding. Keep portable proof in the private report and include only the minimum needed in the tracker.

When updating, preserve history. Add a timestamped note for new evidence, changed severity, accepted risk, fix commit, verification result, release, or deployment. Do not silently rewrite an earlier conclusion. If the finding is disproven, close with the deciding evidence and retain the record.

## Verification and handoff

Read the created or updated record back. Confirm URL/ID, visibility, title, body, labels, status, assignee, and links. Record any platform limitation. Provide the user with the canonical reference and a concise list of mutations.

Do not notify maintainers, submit a bounty report, disclose publicly, merge a fix, or close a report unless those actions were separately requested.
