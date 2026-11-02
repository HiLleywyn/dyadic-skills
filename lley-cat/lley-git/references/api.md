# Git API and recipes

Paths below are relative to `https://git.lley.cat/api`. Send the same Bearer token used for Notes. JSON mutations use `Content-Type: application/json`; script tokens can omit `Origin`. Browser mutations require a permitted HTTPS Origin and owner cookie. URL-encode path/query values.

## Contents

- [Repositories](#repositories)
- [Files and commits](#files-and-commits)
- [Branches and comparisons](#branches-and-comparisons)
- [GitHub](#github)
- [Notebook associations](#notebook-associations)

## Repositories

| Method | Path | Input / result |
| --- | --- | --- |
| GET | `/repositories` | Authorized repository array |
| POST | `/repositories` | Create; returns repository with stable `id` (201) |
| GET | `/repositories/:id` | Metadata and authorized `notes` array |
| PATCH | `/repositories/:id` | Any subset of `name, description, visibility, allowed_cidrs, default_branch` |
| DELETE | `/repositories/:id` | Delete underlying Git repository/reference and associations |
| POST | `/repositories/:id/refresh` | Refresh description/default branch from the backing provider |

Create JSON:

```json
{"name":"experiment","description":"Supplied description","visibility":"private","allowed_cidrs":[],"initialize":true}
```

Names use lowercase letters/digits with `.`, `_` or `-` separators, maximum 100 characters. Descriptions allow 2,000 characters. Set `initialize:false` to push an existing local history into an empty repository. `initialize:true` creates a real README commit on `main`.

Description-only update:

```bash
curl --fail-with-body -sS -X PATCH \
  -H "Authorization: Bearer $LLEY_TOKEN" -H 'Content-Type: application/json' \
  --data '{"description":"Description supplied by the owner"}' \
  "https://git.lley.cat/api/repositories/$REPO_ID"
```

Example IP policy: `{"visibility":"ip","allowed_cidrs":["192.0.2.10/32","2001:db8::/32"]}`. Those are documentation ranges; use the owner's actual permitted addresses. Empty allowlists deny anonymous access. Updating a username or repository name preserves historical remote aliases.

## Files and commits

| Method | Path | Input / result |
| --- | --- | --- |
| GET | `/repositories/:id/files?path=&ref=main` | Directory `{type:"directory",entries:[{name,path,type,size,sha}]}` or file `{type:"file",name,path,size,sha,content}` |
| PUT | `/repositories/:id/files` | `{path,content,branch,message,sha?}`; `content` is base64 bytes, not plain text |
| DELETE | `/repositories/:id/files` | `{path,sha,branch,message}`; commit a file deletion |
| GET | `/repositories/:id/raw?path=README.md&ref=main` | Raw bytes, attachment response |
| GET | `/repositories/:id/archive?ref=main` | ZIP archive |
| GET | `/repositories/:id/commits?ref=main&page=1` | 30 commits/page |
| GET | `/repositories/:id/commit/:sha` | Commit details |

To replace a file: GET it at the desired `ref`, preserve its blob `sha`, encode the new bytes as base64, then PUT with that `sha` and the corresponding branch. To create, omit `sha`. To delete, GET its latest `sha` then DELETE. Paths are repository relative; traversal, backslashes and `.git` components are rejected. Use Git for more than 2 MiB per file or atomic multi-file changes.

The UI renders relative Markdown links against the file's directory and current ref. Root README contents links, `README.md`, nested skills and their references can be browsed without leaving the custom repository interface. Raw API responses return original source.

## Branches and comparisons

| Method | Path | Input / result |
| --- | --- | --- |
| GET | `/repositories/:id/branches` | Up to 100 branch records |
| POST | `/repositories/:id/branches` | `{name:"experiment",from:"main"}`; `git:write` |
| DELETE | `/repositories/:id/branches/:branch` | `repo:admin`; default branch cannot be deleted |
| GET | `/repositories/:id/diff?base=main&head=experiment` | Unified plain-text patch, maximum 5 MB |

A default branch change uses the repository PATCH endpoint. Choose an existing branch. Git clients handle merges and tags; the web UI is a code browser, not an IDE.

## GitHub

```json
{"name":"public-reference","github_url":"https://github.com/OWNER/REPOSITORY","visibility":"public"}
```

This creates a local reference with actual public GitHub metadata and a local UUID. Add `"import":true` to copy history into self-hosted Forgejo instead. GitHub references expose files/history through the local read API; create/write/delete-file and branch mutations require a self-hosted repository. Obtain raw files and archives on GitHub for references. Local visibility does not make an independently public GitHub repository private. Removing a reference leaves the GitHub repository untouched. Unauthenticated GitHub API rate limits apply.

## Notebook associations

`GET /repositories/:id` includes the authorized notebook list. Its entries include notebook `id`, title, slug, cells, `created_at`, `updated_at` and visibility-filtered repository metadata. The native Notes section shows both dates with local 24-hour time and seconds. Public modification times come from published reader snapshots. Its sort selector supports updated/created ascending or descending, title A–Z/Z–A and saved order; `?tab=notes&note_sort=updated-desc` is the default. Other values are `updated-asc`, `created-desc`, `created-asc`, `title-asc`, `title-desc`, `custom`.

```http
PUT /api/associations
Content-Type: application/json

{"repo_id":"REPOSITORY_UUID","note_id":"NOTEBOOK_UUID","position":0}
```

The operation adds a relationship or updates its position. Remove with `DELETE /api/associations/REPOSITORY_UUID/NOTEBOOK_UUID`. Both sides update immediately. Save a complete order atomically with `PUT /api/repositories/REPOSITORY_UUID/notes/order` and `{note_ids:[ALL_CURRENT_NOTEBOOK_UUIDS]}`; each associated UUID must occur exactly once. Duplicates or incomplete/stale membership return `409 ASSOCIATION_CONFLICT`. Ordering requires repository read access and `notes:write` for every note. In the UI choose **Saved order** to enable owner move controls. Reader-local sorting does not change saved positions.

Associations require access to the repository plus notebook write access and a permitted repository scope. A notebook may belong to multiple repositories, including local GitHub references, and is stored independently of Git. Each linked note's **Changes** control opens its revision comparison. The same `notes:read` token can call `GET /api/notebooks/:id/history?view=published` and `GET /api/notebooks/:id/diff?view=published&base=1&head=2`. Read [Notes API](../../lley-notes/references/api.md#publishing-and-recovery) for draft/publication versions and privacy behavior. Unpublished edits do not appear in public diffs.

A notebook may connect to multiple repositories at once. The homepage circular map draws every visible repository-to-note edge, alongside notebook parent/subnote edges. Content bubbles scale using authorized `size_bytes`; repository sizes are provider-reported storage, cached for up to a minute, or null when unavailable.


## Issues And Pull Requests

Under `/repositories/:id`, GET `/issues` or `/pulls` accepts `state=open|closed|all&page=1` (30 rows). Issues exclude pull requests; numbering is shared. POST `/issues` takes `{title,body?,ref?}`; POST `/pulls` takes `{title,body?,head,base}`. GET `/{issues|pulls}/:number` reads the record; PATCH takes `{title?,body?,state?:open|closed}`. GET `/:number/comments?page=1` lists 30 comments and POST takes `{body}`. Use the corresponding `issues:write` or `pulls:write` scope, in addition to Git access.

GET `/pulls/:number/diff` returns actual text. POST `/pulls/:number/merge` takes `{method,head_sha,delete_branch?:false,title?,message?}`. Methods: `merge`, `squash`, `rebase`, `fast-forward-only`. `head_sha` must be the latest reviewed commit. Merge needs `pulls:merge` and `git:write`; branch deletion also needs `repo:admin`. Stale head, conflicts, closed/already merged requests and branch protection are enforced. Force and deferred auto-merge are unavailable.

Typed MCP equivalents: `git_issue_list/get/create/patch/comments/comment`, `git_pull_list/get/create/patch/comments/comment`, `git_pull_diff`, `git_pull_merge`.
