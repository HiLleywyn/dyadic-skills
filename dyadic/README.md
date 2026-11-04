# Dyadic Skills

Official Iris runtime packages are copied from Dyadic's maintained `catalog/skills/`, with metadata and resources intact. Use them through Dyadic's reviewed skill loading and tool-discovery workflows. A skill is guidance, not a callable tool or an authority grant. Live registry schemas and execution-time permissions remain authoritative.

## Official Iris catalog

| Package | Name |
| --- | --- |
| [API Contract Review](iris/api-contract-review/SKILL.md) | API Contract Review |
| [API Integration](iris/api-integration/SKILL.md) | API Integration |
| [Code Review](iris/code-review/SKILL.md) | Code Review |
| [Collaborative Review](iris/collaborative-review/SKILL.md) | Collaborative Review |
| [Compare Documents](iris/compare-documents/SKILL.md) | Compare Documents |
| [CSV Cleanup](iris/csv-cleanup/SKILL.md) | CSV Cleanup |
| [Data Analysis](iris/data-analysis/SKILL.md) | Data Analysis |
| [Data Visualization](iris/data-visualization/SKILL.md) | Data Visualization |
| [Debug Code](iris/debug-code/SKILL.md) | Debug Code |
| [Execution Evidence Review](iris/evidence-review/SKILL.md) | Execution Evidence Review |
| [Explain Code](iris/explain-code/SKILL.md) | Explain Code |
| [Extract Structured Data](iris/extract-structured-data/SKILL.md) | Extract Structured Data |
| [Fact Check](iris/fact-check/SKILL.md) | Fact Check |
| [Forensics](iris/forensics/SKILL.md) | Forensics |
| [Style Guide Editing](iris/house-style/SKILL.md) | Style Guide Editing |
| [Review Imported Instructions](iris/import-review/SKILL.md) | Review Imported Instructions |
| [Meeting Action Items](iris/meeting-actions/SKILL.md) | Meeting Action Items |
| [Requirements to Implementation Plan](iris/requirements-to-implementation-plan/SKILL.md) | Requirements to Implementation Plan |
| [Research Brief](iris/research-brief/SKILL.md) | Research Brief |
| [SQL Analysis](iris/sql-analysis/SKILL.md) | SQL Analysis |
| [Summarize Documents](iris/summarize-documents/SKILL.md) | Summarize Documents |
| [Web Task Automation](iris/web-task-automation/SKILL.md) | Web Task Automation |
| [Write Tests](iris/write-tests/SKILL.md) | Write Tests |

## Security engineering suite

The [Dyadic Security Skills](security/README.md) are owner-authored, Dyadic-native packages added after the pinned official catalog snapshot. They are kept in a separate collection so their provenance is explicit. They use the same runtime principles—live tool discovery, workspace isolation, execution approvals and evidence receipts—but do not imply that a scanner or external disclosure integration is enabled.

| Package | Purpose |
| --- | --- |
| [Security Scan](security/dyadic-security-scan/SKILL.md) | Single-pass repository or component assessment |
| [Security Diff Scan](security/dyadic-security-diff-scan/SKILL.md) | Security review of a patch or revision comparison |
| [Threat Model](security/dyadic-threat-model/SKILL.md) | Assets, actors, trust boundaries, abuse cases and controls |
| [Finding Discovery](security/dyadic-finding-discovery/SKILL.md) | Evidence-linked candidate generation |
| [Attack Path Analysis](security/dyadic-attack-path-analysis/SKILL.md) | Source-to-sink security-boundary tracing |
| [Finding Validation](security/dyadic-finding-validation/SKILL.md) | Skeptical reproduction, counterevidence and verdict |
| [Vulnerability Write-up](security/dyadic-vulnerability-writeup/SKILL.md) | Maintainer-ready private disclosure report |
| [Fix Finding](security/dyadic-fix-finding/SKILL.md) | Minimal remediation and regression coverage |
| [Verify Fix](security/dyadic-verify-fix/SKILL.md) | Independent exploit and behavior verification |
| [Security Hardening](security/dyadic-security-hardening/SKILL.md) | Evidence-to-control architecture roadmap |
| [Security Policy](security/dyadic-security-policy/SKILL.md) | SECURITY.md and disclosure-policy engineering |
| [Track Findings](security/dyadic-track-findings/SKILL.md) | Deduplicated private finding lifecycle |

Install or mirror the security collection with its `_shared/` standards and `scripts/`; the linked evidence, severity, safe-testing and reporting standards are normative parts of the workflows.

## Integration and examples

| Skill | Status |
| --- | --- |
| [Embed Git and Notes](lley-dyadic-embed/SKILL.md) | Host integration scaffold; requires actual identity, vault, tenant and UI integration |
| [Algorithmic Art](examples/algorithmic-art/SKILL.md) | Example with `viewer.html` and its supplied license |
| [Local Field Checks](examples/local-field-checks/SKILL.md) | Example instruction from the portable agent package |

Forensics source-history scanners require an existing local Git worktree; they do not require GitHub. Static API contract audits remain separate from explicitly approved isolated runtime tests. Copying these packages does not enable either plugin or relax their execution boundaries.

See [source provenance](../PROVENANCE.md). Future changes to the 23 official Iris packages belong in Dyadic's source catalog first, followed by a reviewed snapshot update here. The separately identified security suite is maintained directly in this skills repository until it is deliberately adopted into the product catalog.

## Work continuity and operations

[Current Work and delivery workflows](workflows/README.md) cover accepted revisions, artifact handoffs, receipt reconciliation and conflicting supplied sources. [Catalog Maintenance](operators/README.md) covers these three repositories off the platform. These five additions are repository-authored and are not silently represented as installed official defaults.

[Agents](https://git.lley.cat/r/dadd28be-7d91-432f-beb0-00d285e8f02b?ref=store) holds Iris and specialists; [Plugins](https://git.lley.cat/r/ae86ea71-cb4d-4fc5-9ec1-803f8f303989?ref=store) holds the default runtime switches. See [compatibility](../COMPATIBILITY.md) before importing.
