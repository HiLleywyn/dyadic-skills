# Disclosure report standard

## Required report qualities

A disclosure must let a maintainer understand, reproduce, prioritize, and fix the issue without access to the researcher's workstation or unstated context. It must distinguish demonstrated behavior from deployment assumptions and likely impact.

Use this order unless the destination requires a fixed form:

1. **Title** — root cause and impact, not hype.
2. **Executive Summary** — attacker, action, preconditions, boundary crossed, demonstrated impact, affected versions, confidence, and conservative severity.
3. **Background** — only architecture and terminology required to understand the issue.
4. **Vulnerability Details** — source-to-sink trace with repository-relative paths and verified lines or symbols.
5. **Exploitability Analysis** — prerequisites, realistic attack sequence, countercontrols, deployment dependence, and excluded claims.
6. **Proof of Concept** — minimal portable proof using synthetic data, exact setup, expected result, observed result, negative controls, and cleanup.
7. **Remediation** — root-cause fix, regression coverage, compatibility considerations, and optional defense in depth.
8. **Summary** — concise restatement of the supported conclusion.

When the platform separates fields, adapt these sections without dropping their content.

## Title and summary discipline

Prefer “Provider API key returned in external-adapter error response” over “Critical Chainlink takeover.” State the most important prerequisite in the executive summary. If severity depends on Internet exposure or optional configuration, say so in the first paragraph.

## Source references

- Use repository-relative paths, package versions, commit hashes, endpoint names, selectors, or document identifiers.
- Verify one-based lines against the reported revision.
- Include only enough code to explain the flow.
- Do not include local absolute paths, usernames, private repository URLs, tokens, internal hostnames, or unrelated working-tree data.

## Proof of concept

A portable proof:

- uses a synthetic secret, record, account, or identifier;
- binds to loopback or an isolated environment when possible;
- mocks external providers and confirms the mock was consumed;
- names required dependencies and versions;
- limits requests and concurrency;
- includes the assertion that proves the boundary;
- explains cleanup;
- states what it does not prove.

Do not include weaponized persistence, credential theft, reverse shells, bulk enumeration, destructive payloads, or real victim data when a harmless marker establishes the defect.

## Version history

Report the introducing commit and earliest verified affected release when practical. “Current main is affected” is useful but insufficient when maintainers support releases. If no fix exists, say “No fixed release was found in the inspected history,” not “all versions are vulnerable.”

## Severity and excluded claims

Explain why the supported impact fits the chosen severity. Explicitly exclude tempting but unproven claims: no RCE, no SSRF, no silent grant, no cross-tenant access, no public exposure prevalence, or no administrative key scope, as applicable. This makes the report stronger, not weaker.

## Remediation quality

Recommend a root-cause change that preserves intended behavior. Separate required remediation from defense in depth. Define regression tests for the original exploit and adjacent representations or variants. Do not present an untested patch as a verified fix.

## External submission

Draft locally first. Confirm target, program, scope, disclosure channel, identity, attachments, and redactions. Show the final text to the user. Submit, comment, email, create an issue, or publish only when the user explicitly requests that external action and the destination's approval flow is satisfied. Record the resulting report ID or URL without exposing private content.
