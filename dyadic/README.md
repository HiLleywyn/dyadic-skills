# Dyadic Skills

Official Iris runtime packages are copied from Dyadic's maintained `catalog/skills/`, with metadata and resources intact. Use them through Dyadic's reviewed skill loading and tool-discovery workflows. A skill is guidance, not a callable tool or an authority grant. Live registry schemas and execution-time permissions remain authoritative.

The current snapshot has 37 complete catalog packages. [catalog-source.json](catalog-source.json) records the exact Dyadic commit and normalized SHA-256 hashes. The product's [extension architecture](https://git.lley.cat/r/4ae11d0f-eec7-498c-8618-f81c34e29832?ref=docs&path=docs%2Fextension-architecture.md) explains skills, specialist presets, implemented plugins and MCP boundaries; access follows the repository's own permissions.

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
| [Dyadic API Integration](iris/dyadic-api-integration/SKILL.md) | Dyadic API Integration |
| [Dyadic Extension Authoring](iris/dyadic-extension-authoring/SKILL.md) | Dyadic Extension Authoring |
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

The [Dyadic Security Skills](security/README.md) originated as owner-authored packages in this repository and are now adopted into the official Dyadic catalog. Their workflow grouping and attribution remain explicit. They use live tool discovery, workspace isolation, execution approvals and evidence receipts; catalog availability does not enable a scanner or external disclosure integration.

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

Copy the whole individual skill folder. Each security package now contains its own linked standards in `references/` and its finding validator in `scripts/`; it no longer depends on sibling `_shared/` files to work after installation. Cross-skill recommendations require an available installed sibling.

## Integration and examples

| Skill | Status |
| --- | --- |
| [Embed Git and Notes](lley-dyadic-embed/SKILL.md) | Host integration scaffold; requires actual identity, vault, tenant and UI integration |
| [Algorithmic Art](examples/algorithmic-art/SKILL.md) | Example with `viewer.html` and its supplied license |
| [Local Field Checks](examples/local-field-checks/SKILL.md) | Example instruction from the portable agent package |

Forensics source-history scanners require an existing local Git worktree; they do not require GitHub. Static API contract audits remain separate from explicitly approved isolated runtime tests. Copying these packages does not enable either plugin or relax their execution boundaries.

See [source provenance](../PROVENANCE.md). Future changes to all 37 adopted packages belong in Dyadic's source catalog first, followed by `tools/sync_dyadic_skills.py` against this separate checkout. Verify the receipt with `python dyadic/scripts/verify_catalog_mirror.py`. Other workflows and examples remain maintained here.

Owner-started independent tasks currently receive pinned SKILL.md text only. Supply required reference content as selected task inputs when using that mode; full skill resources are available only in workflows that actually load the installed bundle. Mirroring does not install packages into an account or change agent, plugin or MCP selections.
## Work continuity and operations

[Current Work and delivery workflows](workflows/README.md) cover accepted revisions, artifact handoffs, receipt reconciliation and conflicting supplied sources. [Catalog Maintenance](operators/README.md) covers these three repositories off the platform. These five additions are repository-authored and are not silently represented as installed official defaults.

[Agents](https://github.com/HiLleywyn/dyadic-agents) holds Iris and specialists; [Plugins](https://github.com/HiLleywyn/dyadic-plugins) holds the default runtime switches. See the [repository README](../README.md#using-a-skill) before importing.
