# Provenance and Maintenance

## Source snapshots

| Collection | Source | Treatment |
| --- | --- | --- |
| lley.cat | Skills repository through `20f4d1257ff961bd939f3da1ba84e56c3096de65` | Existing skills relocated; current authorization, release and theme guidance corrected |
| Windows, Docker, release verification | The same owner-added commit `20f4d1257ff961bd939f3da1ba84e56c3096de65` | All 13 bundled files preserved byte for byte |
| Official Iris catalog | Dyadic `26ea591af225ed48129a1968db78b3e8f335dc90`, `catalog/skills/` | 23 complete packages copied without modifying their instructions, metadata or scripts |
| Dyadic security engineering suite | Owner-authored in this repository on 2026-11-02 after validated Discourse and Chainlink investigations | 12 original Dyadic-native packages plus shared evidence, authorization, severity, validation and reporting standards; not represented as part of the pinned official catalog snapshot |
| Dyadic examples | Dyadic `e79867312cb9f564c1565cc09f80c2225f298ba7`, `examples/algorithmic-art-skill/` and `examples/agent-package/skills/local-checks/` | Complete example resources retained; readable headings and display metadata added; separated from the official catalog |
| Ward | Ward `30846794c76519729d2564dd70dd34dadfa58105`, `integrations/ward-plugin/skills/ward-scanner/` | Skill and repository MIT license copied from the pinned revision; display name changed to Ward |
| Kali Linux | Owner-installed `kali-linux` skill, metadata version 1.1.0 | Instructions and declared Apache-2.0 license metadata retained; metadata credits `terminal-skills` and links to Kali Linux |
| Karpathy guidelines | Owner-installed `karpathy-guidelines` skill, originally supplied from `multica-ai/andrej-karpathy-skills` | MIT metadata and Karpathy attribution retained |

The local installed Lley Git/Notes skills were compared with this repository. The repository contained newer issues, pull requests, favorites and interface guidance; those additions were preserved rather than replaced by older installed copies.

Displayed names use title case, with the brand written `lley.cat`. Codex-oriented packages have matching `agents/openai.yaml` display names; official Iris packages retain their existing human-readable manifest names. Lowercase frontmatter names, tool identifiers and folder paths remain stable for compatibility. Three imported headings changed for display, and one trailing blank line was removed from Ward's license without changing its terms. Imported text follows the repository's existing LF policy; source comparisons normalize CRLF to LF and record these four presentation edits explicitly.

## Attribution and access

Retain every supplied license and attribution when moving or exporting a package. The algorithmic-art example includes its supplied Apache-2.0 license and Anthropic notice; the Ward package includes its MIT license. Kali and Karpathy originally supplied license declarations in their frontmatter; this collection preserves those declarations without inventing copyright ownership. Publishing this collection does not relicense its contents or expose the underlying private services and data.

Dyadic's copied skills remain snapshots of its maintained runtime packages. Make future runtime edits in Dyadic's source catalog, then update this collection from the reviewed commit. Do not use a copied skill to override live schemas, execution-time authorization or newer user instructions. Product behavior and provider compatibility require their own tests; a well-formed skill alone proves neither.

The security engineering suite is intentionally separated under `dyadic/security/`. It is original workflow content derived from evidence-bounded security practice and the repository owner's requested Dyadic operating model, not a copy of the Codex Security plugin. The suite names connected capability classes but defers to Dyadic's live tool registry and approval policy. Its presence does not authorize live testing, install analyzers, create external reports or change product security state.

## Validation boundaries

The collection was checked for valid skill frontmatter, unique names, working local Markdown links, matching Iris manifest IDs, parseable bundled Python, preserved supporting resources and copied-source integrity under the LF policy above. Existing Windows/Docker/development additions were checked byte for byte against their source commit. No bundled script, installer, scanner or sandbox was executed during collection.

Revalidate moved links and source hashes after updates. Use the existing skill-creator `scripts/quick_validate.py` on each skill folder where available. For `dyadic/security/`, also run `scripts/validate_security_suite.py`; validate durable finding JSON with `scripts/validate_finding.py`. Retain an external receipt listing reviewed source revisions and SHA-256 hashes; do not store credentials, private case evidence or machine-specific token paths in this repository.

## Current collection maintenance

The official 23 packages were re-compared with Dyadic `26ea591af225ed48129a1968db78b3e8f335dc90`; their content remains unchanged. `provenance.json` records every copied source path and SHA-256. The four `dyadic/workflows/` skills and `dyadic/operators/dyadic-catalog-maintenance/` are new repository-authored additions grounded in that revision’s contracts. They have not been added to the product catalog.

The current builders and validator scripts are executed by the repository tests; bundled skill scripts remain inert resources. Security ZIP exports vendor `_shared/` standards and rewrite the documented link prefix in the generated SKILL.md only. Individual archives and the aggregate download are reproducible and have generated checksums. Consult the linked delivery report for this publication’s actual test counts and product limitations.
