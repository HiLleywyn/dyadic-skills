# Provenance

[All Skills](README.md) · [Third-party notices](THIRD_PARTY_NOTICES.md)

## Official Dyadic mirror

The 25 packages under `dyadic/iris/` and the 12 under `dyadic/security/` are complete copies of Dyadic's `catalog/skills/`, written by Dyadic's `tools/sync_dyadic_skills.py`. [dyadic/catalog-source.json](dyadic/catalog-source.json) records the Dyadic revision and the SHA-256 of every mirrored file after UTF-8/LF normalization; `python dyadic/scripts/verify_catalog_mirror.py` checks it without access to the Dyadic repository. [provenance.json](provenance.json) records the same files with their Dyadic source paths and is enforced by `tools/catalog.py check`. Edit these packages in Dyadic, not here.

The security engineering suite was originally authored in this repository and later adopted into Dyadic's catalog, which is now its source. The shared authoring standards in `dyadic/security/_shared/`, `dyadic/security/scripts/` and `dyadic/security/examples/` remain maintained here; each security package also carries its own copies of the references and validators it needs.

## Repository-authored and imported skills

| Skills | Origin | Treatment |
| --- | --- | --- |
| `lley-cat/*` | This repository | Maintained here |
| `windows/*`, `docker/docker-compose-ops`, `development/release-verification` | Owner-added in this repository | Maintained here |
| `dyadic/workflows/*`, `dyadic/operators/dyadic-catalog-maintenance`, `dyadic/lley-dyadic-embed` | Repository-authored for Dyadic | Not part of Dyadic's official catalog |
| `dyadic/examples/algorithmic-art`, `dyadic/examples/local-field-checks` | Dyadic `examples/algorithmic-art-skill/` and `examples/agent-package/skills/local-checks/` at `e79867312cb9f564c1565cc09f80c2225f298ba7` | Resources retained; headings and display metadata added; labeled as examples |
| `ward/ward-scanner` | Ward `integrations/ward-plugin/skills/ward-scanner/` at `30846794c76519729d2564dd70dd34dadfa58105` | Skill and MIT license copied; display name changed to Ward; one trailing blank line removed from the license |
| `linux/kali-linux` | Owner-installed `kali-linux` skill, metadata version 1.1.0 | Instructions and declared Apache-2.0 metadata retained; credits `terminal-skills` |
| `development/karpathy-guidelines` | Owner-installed skill originally from `multica-ai/andrej-karpathy-skills` | MIT metadata and Karpathy attribution retained |

Displayed names use title case with the brand written `lley.cat`. Lowercase frontmatter names, tool identifiers and folder paths stay stable for compatibility.

## Attribution

Retain every supplied license and attribution when moving or exporting a package; see [third-party notices](THIRD_PARTY_NOTICES.md). Publishing this collection does not relicense its contents or expose the private services and data the skills describe. A well-formed skill does not prove that a provider, device or live tool works; product behavior needs its own tests.
