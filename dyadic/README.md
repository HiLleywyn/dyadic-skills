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

## Integration and examples

| Skill | Status |
| --- | --- |
| [Embed Git and Notes](lley-dyadic-embed/SKILL.md) | Host integration scaffold; requires actual identity, vault, tenant and UI integration |
| [Algorithmic Art](examples/algorithmic-art/SKILL.md) | Example with `viewer.html` and its supplied license |
| [Local Field Checks](examples/local-field-checks/SKILL.md) | Example instruction from the portable agent package |

Forensics source-history scanners require an existing local Git worktree; they do not require GitHub. Static API contract audits remain separate from explicitly approved isolated runtime tests. Copying these packages does not enable either plugin or relax their execution boundaries.

See [source provenance](../PROVENANCE.md). Future runtime changes belong in Dyadic's source catalog first, followed by a reviewed snapshot update here.
