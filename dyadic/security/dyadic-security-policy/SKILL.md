---
name: dyadic-security-policy
description: Create or revise a repository SECURITY.md or component security policy covering supported versions, reporting channels, response expectations, safe-harbor testing boundaries, data handling, and disclosure. Use when maintainers want an actionable policy; do not infer legal promises, bounty eligibility, or authorization beyond terms the owner supplies.
---

# Dyadic Security Policy

Write a policy that helps researchers report safely and helps maintainers triage consistently. The policy is operational and security guidance, not legal advice. Never invent safe-harbor commitments, payment terms, response SLAs, encryption keys, contacts, or authorized assets.

Read [safe testing](references/safe-testing.md), [report standard](references/report-standard.md), and existing repository/community guidance.

## Gather authoritative inputs

Identify:

- project owner and policy authority;
- supported release branches and end-of-life versions;
- private reporting channel and monitored contact;
- vulnerability platform or security-advisory workflow;
- in-scope repositories, packages, domains, apps, APIs, devices, contracts, and testnets;
- explicitly excluded third parties and environments;
- allowed and prohibited techniques;
- test account and identification-header requirements;
- handling rules for personal data, secrets, funds, and customer content;
- acknowledgment, status-update, remediation, and disclosure expectations;
- bounty or credit terms only when documented by the owner;
- relevant licenses, contributor agreements, and coordinated-disclosure constraints.

If these facts are missing, insert clearly labeled owner decisions instead of plausible values.

## Required policy sections

### Supported versions

Provide a simple table tied to maintained branches/releases. Explain how security fixes are backported and how users learn which version contains a fix.

### Reporting a vulnerability

Name one preferred private channel and a fallback. Request target, revision/version, summary, prerequisites, steps, impact, proof, and contact preference. Tell reporters not to include real secrets or unnecessary personal data. Provide the public-key fingerprint only if the owner supplies and verifies it.

### Scope

List assets precisely. Repository scope does not imply every deployment; a domain scope does not imply third-party SaaS behind it. Define testnet/mainnet and hardware boundaries where applicable.

### Research rules

State permitted low-volume, good-faith techniques and explicit prohibitions: denial of service, social engineering, physical intrusion, credential attacks, malware, persistence, customer-data access, mainnet value movement, destructive actions, bulk scanning, or third-party targeting, as the owner decides. Define request, account, and cost limits when relevant.

### Safe harbor

Include only language approved by the owner or counsel. Scope it to good-faith research that follows the policy, minimizes harm, stops on sensitive data, and reports promptly. Do not promise immunity from third-party claims or laws outside the owner's control.

### Response and disclosure

Describe acknowledgment and update targets as goals unless contractually guaranteed. Explain duplicate handling, severity review, remediation coordination, CVE/advisory process, credit preferences, and coordinated public disclosure. Avoid requiring silence indefinitely.

### Data handling

Tell researchers to use synthetic data, minimize collection, encrypt sensitive evidence in transit, delete retained data after resolution, and never use discovered credentials. Provide a stop-and-report path for accidental customer-data exposure.

## Repository integration

Check links from README, contribution docs, package metadata, website security contact, and `.well-known/security.txt` when in scope. Do not create or alter these files unless the user asks. Keep contact and scope information consistent across locations.

## Review

Validate that the policy is specific, internally consistent, and implementable by the maintainer team. Flag owner decisions and legal-review items. Provide a change summary when revising an existing policy and preserve valid commitments. Do not publish, commit, or announce the policy unless requested.

## Installed Resources

Use `tools.load(inventory=true)` to discover enabled skills and permitted tools. Load the skills group,
then read this package with `skills.read(name="dyadic-security-policy", path="SKILL.md")`.
Read linked references using the same skill name and their bundle-relative paths. Cross-skill `$name`
references describe optional workflows, not callable tool names; discover an enabled sibling first.
If it is unavailable, perform the supported part directly and record the remaining phase as unexecuted.

For a durable record, use the [finding schema](references/finding.schema.json). The bundled
[validator](scripts/validate_finding.py) checks record invariants without third-party packages; it does
not establish that a finding is true. Run it only through an authorized execution tool.
