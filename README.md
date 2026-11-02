# Platform skills

AI instructions for the actual lley.cat API, Git gateway, and notebook format. These skills work from a checkout or by reading their files through the repository API. They do not contain credentials.

Windows, Docker, and general development skills are grouped by domain below. Each skill directory contains its own `SKILL.md` and any supporting files.

## Contents

| Skill | Use it for | Detailed reference |
| --- | --- | --- |
| [lley-interface](lley-interface/SKILL.md) | Exact Dyadic design system, themes, responsive navigation, shared cards/controls and visual validation | Interface contract in the skill |
| [lley-profile](lley-profile/SKILL.md) | Public profile, independent pins, real contribution history and avatar navigation | Profile API and privacy rules in the skill |
| [lley-git](lley-git/SKILL.md) | Repositories, descriptions, visibility, files, branches, commits, clone/push, GitHub references, notebook associations | [Git API and recipes](lley-git/references/api.md) |
| [lley-notes](lley-notes/SKILL.md) | Notebook CRUD, nested subnotes, cells, execution/validation, publishing, attachments, revisions, export, multiple repository associations | [Cell format and execution](lley-notes/references/cells.md), [Notes API and recipes](lley-notes/references/api.md) |
| [lley-delivery](lley-delivery/SKILL.md) | Custom Actions, stage graphs, CI/CD, isolated runners, logs, artifacts and Releases | [Delivery API and format](lley-delivery/references/api.md) |
| [lley-mcp](lley-mcp/SKILL.md) | Typed MCP tools, protected-file token setup, safe notebook patches and append-only bridge messaging | [Platform MCP contract](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?path=docs%2FMCP.md) |
| [lley-dyadic-embed](lley-dyadic-embed/SKILL.md) | Portable host-authenticated Git and rich Notes backend/React integration, separate branch, workspace/vault seams | Package README on the integration branch |
| [lley-android](lley-android/SKILL.md) | Capacitor app across all three sites, Android builds/signing, native haptics, notifications and document storage | Native paths and build procedure in the skill |

### Windows

| Skill | Use it for |
| --- | --- |
| [windows-sandbox](windows/windows-sandbox/SKILL.md) | Disposable Windows desktops, `.wsb` files, guest scripts, folder mappings, setup and CLI automation |
| [wsl-ops](windows/wsl-ops/SKILL.md) | Distribution selection, Windows/Linux paths, shell environment, networking, interoperability and recovery |
| [windows-diagnostics](windows/windows-diagnostics/SKILL.md) | Processes, ports, file locks, events, services, scheduled tasks and Sysinternals investigations |
| [winget-setup](windows/winget-setup/SKILL.md) | Exact package selection, requested installations/updates, pins, environment export/import and Sandbox bootstrap |

### Docker

| Skill | Use it for |
| --- | --- |
| [docker-compose-ops](docker/docker-compose-ops/SKILL.md) | Service health, DNS/networks, persistent data, environment preservation and targeted recreation |

### Development

| Skill | Use it for |
| --- | --- |
| [release-verification](development/release-verification/SKILL.md) | Source/artifact/runtime identity, readiness, API behavior and visible user outcomes after delivery |

For local Codex use, copy the individual skill directory containing `SKILL.md` into your configured skills directory (normally `~/.codex/skills`). The category directories organize this repository; install a skill such as `windows/wsl-ops` as `~/.codex/skills/wsl-ops`.

```text
skills/
├── README.md
├── lley-interface/SKILL.md
├── lley-profile/SKILL.md
├── lley-mcp/SKILL.md
├── lley-dyadic-embed/SKILL.md
├── lley-android/SKILL.md
├── lley-delivery/
│   ├── SKILL.md
│   └── references/api.md
├── lley-git/
│   ├── SKILL.md
│   └── references/api.md
├── lley-notes/
│   ├── SKILL.md
│   └── references/
│       ├── api.md
│       └── cells.md
├── windows/
│   ├── windows-sandbox/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/cli.md
│   ├── wsl-ops/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── windows-diagnostics/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   └── winget-setup/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── docker/
│   └── docker-compose-ops/
│       ├── SKILL.md
│       └── agents/openai.yaml
└── development/
    └── release-verification/
        ├── SKILL.md
        └── agents/openai.yaml
```

## Quick reference

Every domain serves the same `/api` contract. Prefer `https://git.lley.cat/api` for repository work and `https://notes.lley.cat/api` for notebook work. Authenticate API calls with `Authorization: Bearer $LLEY_TOKEN`. Use that same token as the password for Git HTTPS. Obtain it through [Settings → Security → Access Tokens](https://lley.cat/settings/security#access-tokens); a token cannot mint other tokens.

| Task | Scopes to select |
| --- | --- |
| Clone, inspect private code, raw files, archives | `git:read` |
| Push; create, replace or delete files; create branches | `git:read`, `git:write` |
| Create/delete/rename repositories; descriptions, visibility, default branch; delete branches | `git:read`, `repo:admin` |
| Read drafts, saved output, attachments and exports | `notes:read` |
| Create/edit/delete notebooks, cells, attachments and associations; restore revisions | `notes:read`, `notes:write` |
| Publish/update/unpublish a notebook | `notes:read`, `notes:publish` (add `notes:write` to edit first) |
| Associate notes with private repositories | `git:read`, `notes:read`, `notes:write` |
| All repository and notebook operations | All six Git/repository/Notes scopes above |
| Edit profile and current project | `profile:write` |
| Read Actions configuration, runs, logs and artifacts | `actions:read` |
| Create/edit issues or pull requests | `git:read` + `issues:write` / `pulls:write` |
| Merge reviewed pull request head | `git:read`, `git:write`, `pulls:merge`; add `repo:admin` to delete the source branch |
| Configure Actions | `actions:write` |
| Credential metadata / encrypted writes and environment policies | `secrets:read` / `secrets:write` |
| Read / change owner repository and note favorites | `stars:read` / `stars:write` |
| Start/cancel/retry Actions when explicitly enabled | `actions:run` |
| Read published releases/assets | `releases:read` |
| Create/edit/publish/delete releases and upload/delete assets | `releases:write` |

Scopes are independent. Repository restrictions also apply to notebook associations. Creating a repository requires **unrestricted** `repo:admin`; a repository-limited token cannot create its own new target. A restricted Notes token must create a notebook with at least one permitted `repository_ids` entry. Profile permission is global only.

Discover the current scope descriptions with `GET /api/token-permissions`. The owner can edit token names, scopes, repository limits and expiry in Settings without changing the token string. Changes and revocation apply on the next request. Rotation revokes the old string and displays a replacement once.

## Working conventions

**Only lley-cat is authorized for production delivery verification.** Keep every other repository disabled with its triggers off. Global resume and repository activation are separate owner-only gates. Use isolated tests before production runs. Previewing stages, source pushes or release publication do not authorize activating additional repositories. Work on the platform must be documented in notes associated with lley-cat. Dyadic is read-only reference; only change explicitly authorized repositories.

- Use returned UUIDs, not names, as resource identifiers. Renames preserve aliases and stable links.
- Read a notebook before modifying it. Supply its latest `version`; merge after `409 VERSION_CONFLICT`.
- Draft edits and publishing are separate. Only an explicit publish operation updates the reader snapshot.
- Verify mutations by reading the changed resource. For deletion, verify absence using a credential that could access it before deletion.
- Keep credentials in the environment or credential manager; do not put them in remotes, committed files, command output, or notebook cells.

The complete platform contract is in [docs/API.md](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?tab=files&ref=main&path=docs%2FAPI.md). Deployment belongs to [operations](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?tab=files&ref=main&path=docs%2FOPERATIONS.md), outside these application-use skills.
