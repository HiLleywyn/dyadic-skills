# Dyadic Skills

[Skills](README.md) · [Agents](https://git.lley.cat/r/dadd28be-7d91-432f-beb0-00d285e8f02b?ref=main) · [Plugins](https://git.lley.cat/r/ae86ea71-cb4d-4fc5-9ec1-803f8f303989?ref=main)

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

The [Dyadic catalog](dyadic/README.md) mirrors 37 official skills: 25 under Iris and 12 in the [security engineering suite](dyadic/security/README.md). Four [Current Work and delivery workflows](dyadic/workflows/README.md), a [catalog-maintenance operator skill](dyadic/operators/README.md), two bundled examples and the [Git/Notes embedding skill](dyadic/lley-dyadic-embed/SKILL.md) remain separate repository-authored additions or examples.

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

See [provenance and maintenance](PROVENANCE.md) for source revisions, attribution and validation boundaries. This collection has 61 skills; load only those relevant to the task. Run `python dyadic/scripts/verify_catalog_mirror.py` to verify the recorded catalog snapshot.

## Validation and packages

[Catalog inventory](catalog.json) · [Maintenance](MAINTENANCE.md) · [Compatibility](COMPATIBILITY.md) · [Delivery report](https://git.lley.cat/r/dadd28be-7d91-432f-beb0-00d285e8f02b?path=REPORT.md&ref=main)

With Python 3.11+ and PyYAML, run `python tools/catalog.py check`, `python .lley/run.py`, then `python tools/catalog.py build`. Each `dist/<skill-id>.zip` is an individual importable skill; `dist/collection.zip` groups them for download and must be extracted first. The security exports include shared standards inside each ZIP. The original source layout and existing package IDs remain unchanged.

## Source, mirrors and licensing

The [lley.cat repository](https://git.lley.cat/r/1a151e58-468a-45f1-a028-92c95690ad68) is canonical. [HiLleywyn/dyadic-skills](https://github.com/HiLleywyn/dyadic-skills) is a secondary source mirror with the same catalog and Git history.

Project-authored instructions, documentation and tooling use [MIT](LICENSE). Bundled third-party material retains its original licenses and attribution; see [third-party notices](THIRD_PARTY_NOTICES.md). A repository license does not grant access to connected services, proprietary tools or somebody else's data.

## Choose the right package

| Need | Start here | Required environment |
|---|---|---|
| Work inside Dyadic | [Official Iris skills](dyadic/README.md) | Dyadic's reviewed package import and the selected tools |
| Run an evidence-bounded review | [Security workflows](dyadic/security/README.md) | The tools and authorization declared by the chosen workflow |
| Maintain Lley Git, Notes or Releases | [Lley platform skills](lley-cat/README.md) | An owned account and the specific API scopes in each skill |
| Operate a Windows machine | [Windows workflows](windows/README.md) | An authorized local environment; each workflow discovers its own prerequisites |
| Verify a release | [Release verification](development/release-verification/SKILL.md) | A known source revision, artifact and intended destination |

Read `SKILL.md` before running bundled resources. Preserve the whole package directory: references, templates, scripts, metadata and notices are part of the workflow. A category directory is navigation, not an installable skill. The machine-readable [catalog](catalog.json) is the searchable inventory, and [provenance](PROVENANCE.md) explains which packages are official snapshots versus repository additions.

## Author and verify a change

For an official Dyadic package, change its authoritative platform source first, then refresh the exact snapshot receipt. For a repository-authored skill, edit its own `SKILL.md` and supporting resources. Keep the existing package ID and resource links stable.

```sh
git clone https://github.com/HiLleywyn/dyadic-skills.git
cd dyadic-skills
python -m pip install PyYAML
python tools/catalog.py check
python .lley/run.py
python tools/catalog.py build
```

The checker validates instruction structure, IDs, links, provenance and packaged resources. Builders create reproducible archives without executing downloaded skill scripts. Tests and import inspection establish package compatibility; they do not establish that a provider, physical device or live external tool works. [Maintenance](MAINTENANCE.md) documents the complete refresh and export sequence.

For platform capabilities and current schemas, use [Dyadic Developers](https://dyadic.app/developers/). For durable workflow orchestration, see [Matrix](https://dyadic.app/developers/matrix/) and its [auditable engine](https://github.com/HiLleywyn/dyadic-matrix). [Agents](https://github.com/HiLleywyn/dyadic-agents) define identities and delegated roles; [plugins](https://github.com/HiLleywyn/dyadic-plugins) describe actual tool switches.
