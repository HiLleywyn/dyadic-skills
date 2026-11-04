# Provenance and Maintenance

## Current Dyadic Catalog Snapshot

The `docs` refresh adopts the twelve owner-authored security workflows into Dyadic and mirrors 37 complete official packages back here: 25 under `dyadic/iris/` and 12 under `dyadic/security/`. [dyadic/catalog-source.json](dyadic/catalog-source.json) records the exact merged Dyadic source commit and every mirrored file's SHA-256 after UTF-8/LF normalization. `python dyadic/scripts/verify_catalog_mirror.py` verifies that receipt without access to the private source repository.

The security suite is 1.0.1: supported catalog icons/colors, complete package-local references and validators, explicit resource discovery and optional cross-skill routing. Store metadata does not turn a package on for every account. Dyadic API Integration and Dyadic Extension Authoring are new 1.0.0 packages; API Integration and API Contract Review are revised to 1.0.1. Catalog punctuation follows the product's existing rules. Original authorship and the platform/workflow layout remain intact.

The source catalog is now authoritative for all 37 adopted packages. The original `_shared/` authoring standards, examples and unrelated skills remain in this repository. Existing user installations and service configuration are outside this mirror operation. Skill, ZIP/resource, finding-validator and source-equality checks establish packaging consistency; the independent authoring exercise and documented runner limits do not establish deployed model quality.

## Earlier Source Snapshots

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

The merged collection retains the `store` branch's four `dyadic/workflows/` skills and `dyadic/operators/dyadic-catalog-maintenance/`, grounded in Dyadic `26ea591af225ed48129a1968db78b3e8f335dc90`. These five repository-authored additions have not been added to the product catalog. The `docs` snapshot supersedes the earlier 23-package mirror: `provenance.json` and `dyadic/catalog-source.json` now agree on all 149 source files in 37 packages at Dyadic `ae1c3e2119d85f518885b253132adad4110d4787`.

The current builders and validator scripts are executed by the repository tests; bundled skill scripts remain inert resources. Security ZIP exports retain the complete package-local references and validators. The existing shared builder also includes the original authoring standards under `references/standards/`; current instructions link to the package-local references, and their bytes are unchanged in exports. Individual archives and the aggregate download are reproducible and have generated checksums. Consult [verification evidence](verification/README.md) for the merged collection's results and the linked Store delivery report for its historical validation boundaries.
