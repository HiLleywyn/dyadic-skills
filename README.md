# Skills

[Skills](README.md) · [Agents](https://git.lley.cat/r/dadd28be-7d91-432f-beb0-00d285e8f02b?ref=store) · [Plugins](https://git.lley.cat/r/ae86ea71-cb4d-4fc5-9ec1-803f8f303989?ref=store)

Maintained instructions for lley.cat, Dyadic, Ward, Windows, Linux, Docker and development. Each skill folder contains its own `SKILL.md` and supporting resources. This collection contains guidance and examples, not credentials or installed services. Repository visibility is managed separately by its owner.

## lley.cat

| Skill | Purpose |
| --- | --- |
| [lley.cat Git](lley-cat/lley-git/SKILL.md) | Git gateway, repositories, files, branches, issues and pull requests |
| [lley.cat Notes](lley-cat/lley-notes/SKILL.md) | Rich notebooks, cells, outputs, versions, publishing and associations |
| [lley.cat Interface](lley-cat/lley-interface/SKILL.md) | Shared themes, responsive controls, navigation and visual verification |
| [lley.cat Profile](lley-cat/lley-profile/SKILL.md) | Profile, pins, contribution history and privacy |
| [lley.cat Actions and Releases](lley-cat/lley-delivery/SKILL.md) | Custom Actions, isolated jobs, reports, artifacts and Releases |
| [lley.cat MCP](lley-cat/lley-mcp/SKILL.md) | Streamable HTTP/Bearer setup and typed platform operations |
| [lley.cat Android](lley-cat/lley-android/SKILL.md) | Native shell, signing, emulator verification and release publication |

The [lley.cat reference](lley-cat/README.md) includes scopes and working conventions. These skills describe the custom gateway, not generic Forgejo administration.

## Dyadic

The [Dyadic catalog](dyadic/README.md) contains 23 official Iris skills, a 12-skill [security engineering suite](dyadic/security/README.md), four [Current Work and delivery workflows](dyadic/workflows/README.md), a [catalog-maintenance operator skill](dyadic/operators/README.md), two bundled examples and the [Git/Notes embedding skill](dyadic/lley-dyadic-embed/SKILL.md).

Iris skills retain their `skill.json` metadata and bundled resources. They depend on Dyadic's existing tool registry, execution broker, sandbox and approval system. Reading a skill elsewhere does not provide those tools or authorize their execution. The security suite adds full workflows for scanning, threat modeling, candidate discovery, attack-path analysis, validation, reporting, remediation, verification, hardening, policy and finding lifecycle. The embedding package remains an integration scaffold, not a claim of a deployed Dyadic installation.

## Ward

| Skill | Purpose |
| --- | --- |
| [Ward](ward/ward-scanner/SKILL.md) | Bounded static repository/hash analysis, scan history and evidence-based verdicts |

Ward's skill requires a connected Ward MCP service. The skill folder does not install the scanner. An `unknown` or incomplete scan is never evidence that a repository is safe.

## Windows

| Skill | Purpose |
| --- | --- |
| [Windows Sandbox](windows/windows-sandbox/SKILL.md) | Disposable desktops, `.wsb` files, mappings and guest automation |
| [WSL Operations](windows/wsl-ops/SKILL.md) | Distributions, paths, networking, interoperability and recovery |
| [Windows Diagnostics](windows/windows-diagnostics/SKILL.md) | Processes, ports, locks, events, services and scheduled tasks |
| [WinGet Setup](windows/winget-setup/SKILL.md) | Exact package selection, requested updates, pins and environment import/export |

## Docker and Linux

| Skill | Purpose |
| --- | --- |
| [Docker Compose Operations](docker/docker-compose-ops/SKILL.md) | Service health, DNS, persistent data and targeted recreation |
| [Kali Linux](linux/kali-linux/SKILL.md) | Authorized security labs, distribution setup and bounded tool selection |

## Development

| Skill | Purpose |
| --- | --- |
| [Release Verification](development/release-verification/SKILL.md) | Source, artifact and runtime identity; readiness and visible delivery |
| [Karpathy Guidelines](development/karpathy-guidelines/SKILL.md) | Surgical changes, explicit assumptions and verifiable outcomes |

## Use and installation

Read only the relevant skill and its requested references. For local Codex installation, copy the whole individual skill folder into the configured skills directory, normally `~/.codex/skills/<skill-name>`. For example, `windows/windows-sandbox/` becomes `~/.codex/skills/windows-sandbox/`, including `references/` and `agents/`. Category folders are for organization; they are not skill packages themselves.

Lley skills link to complementary sibling skills. Install the relevant siblings together or read them in this checkout. Dyadic's Iris packages use its existing reviewed import/installation workflow; preserve `skill.json`, scripts, templates and licenses. The two example packages are labeled separately from the official catalog. Do not run downloaded scripts merely to install or inspect a skill.

Installation does not change model selections, enable plugins, grant permissions, activate CI, publish notebooks or launch a sandbox. Those actions follow the user's actual task authorization and the destination's enforcement.

## Moved paths

The seven former root `lley-*` folders now live under `lley-cat/`. `lley-dyadic-embed/` moved to `dyadic/lley-dyadic-embed/`. Skill names are unchanged; update folder import URLs accordingly. Historical commit URLs remain available in Git history. Windows, Docker and release-verification additions retain their existing paths.

See [provenance and maintenance](PROVENANCE.md) for source revisions, attribution and validation boundaries. This collection has 59 skills; it does not imply that 54 skills should be loaded into every conversation.

## Validation and packages

[Catalog inventory](catalog.json) · [Maintenance](MAINTENANCE.md) · [Compatibility](COMPATIBILITY.md) · [Delivery report](https://git.lley.cat/r/dadd28be-7d91-432f-beb0-00d285e8f02b?path=REPORT.md&ref=store)

With Python 3.11+ and PyYAML, run `python tools/catalog.py check`, `python .lley/run.py`, then `python tools/catalog.py build`. Each `dist/<skill-id>.zip` is an individual importable skill; `dist/collection.zip` groups them for download and must be extracted first. The security exports include shared standards inside each ZIP. The original source layout and existing package IDs remain unchanged.
