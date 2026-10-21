---

name: lley-git

description: Use git.lley.cat to create and manage repositories, inspect and commit files, push or clone over HTTPS, manage branches and visibility, track issues and pull requests, merge reviewed commits, and associate notebooks. Applies to the custom lley.cat Git gateway, not generic GitHub account administration or infrastructure changes.

---

# Git on lley.cat

Use the public gateway at `https://git.lley.cat/api`. It fronts a private Forgejo engine; do not use Forgejo account, token, or `/api/v1` endpoints. This platform has one owner. Public readers need no account; authenticated automation uses an owner-issued personal access token.

When available, use the [typed MCP tools](../lley-mcp/SKILL.md) for API operations. Git HTTPS remains the transport for normal clone/push. The MCP adapter reads its token from a protected file or client vault; do not move it into shell arguments.

Read [API and recipes](references/api.md) for endpoint payloads, file commits, branches, GitHub imports and associations. For writing notebook content or execution outputs, also use [lley-notes](../lley-notes/SKILL.md).

Every repository has custom **Actions** and **Releases** sections. Use [lley-delivery](../lley-delivery/SKILL.md) for stage graphs, CI/CD, logs, artifacts and versioned releases. They use new independent `actions:read`, `actions:write`, `actions:run`, `releases:read` and `releases:write` grants. Existing Git scopes do not silently grant these permissions. Delivery is currently required to stay paused with every trigger disabled; pushing source must not activate it.

## Authentication and discovery

Use `Authorization: Bearer $LLEY_TOKEN` for API requests. Git HTTPS accepts the same token as its password; the username can be the owner's current username. Keep credentials in a credential manager or process environment, never in a remote URL, logs or repository files.

```bash

curl --fail-with-body -sS -H "Authorization: Bearer $LLEY_TOKEN" \

  https://git.lley.cat/api/repositories

```

Tokens are issued and edited in `https://lley.cat/settings/security#access-tokens` → Access Tokens. `GET /api/token-permissions` discovers current permissions. Token management and passkey endpoints require an owner browser session; an API token cannot promote itself or create another token.

Choose independent scopes for the requested work:

| Operation | Scopes |

| --- | --- |

| Read private metadata, files, history, diffs, raw/archive, clone/pull | `git:read` |

| Push, create/replace/delete files, create branch | `git:read` + `git:write` |

| Create/delete/rename repositories, description/settings/default branch, delete branch, refresh | `git:read` + `repo:admin` |

| Link or unlink notebooks | `git:read` + `notes:read` + `notes:write` |

A repository-limited token cannot create repositories. Use unrestricted `repo:admin` for creation, then restrict a token to the returned UUID when appropriate. A Notes scope never grants Git read access.

## Stable identity and Git

Find the requested repository in the authorized list and use its `id` everywhere. Names/slugs can change; previous names remain aliases and cannot be reused by another repository while reserved.

- Detail page: `https://git.lley.cat/r/REPOSITORY_UUID`

- Stable remote: `https://git.lley.cat/r/REPOSITORY_UUID.git`

- Human remote: `https://git.lley.cat/USERNAME/REPOSITORY_SLUG.git`

Use normal Git for existing local projects, multi-file changes, merges, history and large files. A newly created `initialize:false` repository is empty: make a local commit, select `main`, add its stable remote and push. An initialized repository already has a README commit; clone/fetch it before pushing to avoid unrelated histories. Respect local changes and remote history; do not force-push as a routine upload.

Browser/API file commits are limited to 2 MiB per file. `PUT /repositories/:id/files` creates when `sha` is omitted and replaces when the current blob `sha` is supplied. `DELETE` on the same endpoint requires the current `sha`, branch and commit message. These operations create real commits; deletion preserves historical content.

## Management and visibility

Create with `POST /repositories`. Use **partial** `PATCH /repositories/:id` for descriptions, names, visibility, CIDRs or default branch; omitted fields remain unchanged. Deleting with `DELETE /repositories/:id` deletes Git storage and associations but leaves the independent notebooks themselves intact. Make that deletion only when the user's task authorizes it and verify the exact UUID.

Visibility values are `public`, `private`, `ip`. IP restrictions accept IPv4 and IPv6 addresses/CIDRs. They protect local metadata, files, raw/archive and Git HTTP. An authorized owner or suitably scoped token retains access. Do not forge forwarding headers or alter ingress to work around a denial.

`provider:github` means a public GitHub **reference**, read only here. Its local page supports notebook associations. To host an editable copy, create with `github_url` and `import:true`. This does not grant access to private GitHub repositories or allow changes to GitHub itself.

## Verify the result

Repository **Tests** shows actual case results and Actions history. The SVG badge at `/api/repositories/:id/badges/tests.svg` uses repository/IP permissions, reports absent tests honestly and marks results outdated when the source commit changes. Use the delivery skill for report ingestion; do not fabricate a passing badge. Owner favorites use `GET/PUT/DELETE /repositories/:id/star` with independent `stars:read`/`stars:write` scopes. `GET /stars` lists readable favorites within the token’s repository restrictions. This is one owner's synchronized state, not public visitor accounts or invented community counts.

Read back changed metadata and affected files/branches. After a Git push, fetch or clone and inspect the resulting commit. Repository pages and lists display actual modification timestamps with seconds in the viewer's local 24-hour time. Do not generate repository descriptions or notes unless the user requested that content.

Errors use `{error:{code,message}}`. `401` means invalid/expired/revoked credentials, `404` can conceal an unauthorized private resource, `409` indicates a name/branch/file conflict. Check the token's read/write/admin scopes and repository restriction before treating 404 as proof that a resource does not exist. Re-read the current file SHA after a conflict; do not blindly overwrite concurrent work.



## Issues, Pull Requests And Favorites

Hosted repositories have real Issues and Pull Requests in the current branch's **Main** menu. Use `git:read` for private content, independent `issues:write` or `pulls:write` for mutations, and `pulls:merge` plus `git:write` for merging. Deleting the merged source branch also requires `repo:admin`. Existing tokens must explicitly receive these scopes; they are not inferred from Git writing. Read the API reference for payloads.

Read the actual pull diff and latest head before a merge. Supply the exact reviewed SHA; after `HEAD_CHANGED`, reload and review. Never pass force flags or assume CI succeeded because merge is available. Creating a PR does not authorize merging it or activating delivery. Comments require the user's communication authorization. Public/IP/private access gates cover these endpoints, and GitHub references stay read only.

The repository list uses **All / Starred** beside Search. `stars:read` and `stars:write` manage owner favorites with independent repository read access. **Automations** contains **Actions** and **Tests**; **Credentials** appears only for the owner. Branch names are shown verbatim and selecting a branch opens its own files.

## Repository Layout

Use the shared content inset (Dyadic’s clamp(1rem, 4vw, 3rem)) inside full-width surfaces. The header places a compact clone field beside its title at the top-right. Description spans the header; Updated/tests sit directly left of Star, Upload, Download and Settings. Upload/Download are icon-only and accessible by label. Remove the old separate clone toolbar, manual Refresh control and duplicate branch/upload toolbar below the menu. The branch/menu still selects the actual ref; repository sections stay on one line. Poll read data every 15 seconds while visible and on focus/visibility return. Pause file refresh during editing, preserve unchanged data objects and cancel obsolete requests; update README when its blob changes. Do not trigger CI, fabricate updates or edit repository data to demonstrate a layout.

Library controls place Add Repository at the title’s upper right and All/Starred beside Search. Entry stars/available tests belong at the top-right, with descriptions beneath across the width. Repository navigation retains icons, fills its width, and keeps dropdowns on-screen. Clone is at the header’s upper right; Updated/tests sit left of Star, Upload, Download and Settings. Save controls float only for actual pending changes.


Interface work follows [lley-interface](../lley-interface/SKILL.md): the current Dyadic Workspace source, Geist/Geist Mono, shared Dark/Light/OLED roles, responsive rail/drawer, bounded menus and common cards/controls. Settings → Security contains Access Tokens. Preserve platform authorization and authored content while changing the UI.
