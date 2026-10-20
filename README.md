# Platform skills

AI instructions for the actual lley.cat API, Git gateway, and notebook format. These skills work from a checkout or by reading their files through the repository API. They do not contain credentials.

## Contents

| Skill | Use it for | Detailed reference |
| --- | --- | --- |
| [lley-git](lley-git/SKILL.md) | Repositories, descriptions, visibility, files, branches, commits, clone/push, GitHub references, notebook associations | [Git API and recipes](lley-git/references/api.md) |
| [lley-notes](lley-notes/SKILL.md) | Notebook CRUD, nested subnotes, cells, execution/validation, publishing, attachments, revisions, export, multiple repository associations | [Cell format and execution](lley-notes/references/cells.md), [Notes API and recipes](lley-notes/references/api.md) |
| [lley-delivery](lley-delivery/SKILL.md) | Custom Actions, stage graphs, CI/CD, isolated runners, logs, artifacts and Releases | [Delivery API and format](lley-delivery/references/api.md) |
| [lley-mcp](lley-mcp/SKILL.md) | Typed MCP tools, protected-file token setup, safe notebook patches and append-only bridge messaging | [Platform MCP contract](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?path=docs%2FMCP.md) |
| [lley-android](lley-android/SKILL.md) | Capacitor app across all three sites, Android builds/signing, native haptics, notifications and document storage | Native paths and build procedure in the skill |

```text
skills/
├── README.md
├── lley-android/SKILL.md
├── lley-delivery/
│   ├── SKILL.md
│   └── references/api.md
├── lley-git/
│   ├── SKILL.md
│   └── references/api.md
└── lley-notes/
    ├── SKILL.md
    └── references/
        ├── api.md
        └── cells.md
```

## Quick reference

Every domain serves the same `/api` contract. Prefer `https://git.lley.cat/api` for repository work and `https://notes.lley.cat/api` for notebook work. Authenticate API calls with `Authorization: Bearer $LLEY_TOKEN`. Use that same token as the password for Git HTTPS. Obtain it through [Settings → Access tokens](https://lley.cat/admin); a token cannot mint other tokens.

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
| Configure Actions | `actions:write` |
| Credential metadata / encrypted writes and environment policies | `secrets:read` / `secrets:write` |
| Read / change owner repository favorites | `stars:read` / `stars:write` |
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
