---
name: lley-notes
description: Create, edit, publish, export and recover notebooks on notes.lley.cat, including its custom cell schema, JavaScript/Python browser execution, rich saved outputs, attachments and repository associations. Use for this platform rather than Jupyter notebooks or arbitrary server execution.
---

# Notes on lley.cat

Use `https://notes.lley.cat/api` with `Authorization: Bearer $LLEY_TOKEN`. The same personal access token works for Git HTTPS and Notes; there is no separate Notes credential or Jupyter service.

- Read [Notes API and recipes](references/api.md) for notebook and cell CRUD, publishing, revision history/diffs, uploads, exports and associations.
- Read [Cell format and execution](references/cells.md) before authoring cells, code, attachments, charts or saved outputs. The custom format and runtime helpers matter here.
- Use [lley-git](../lley-git/SKILL.md) when creating or modifying associated repositories.
- Use [lley-android](../lley-android/SKILL.md) for Notes in the native app and [lley-delivery](../lley-delivery/SKILL.md) for documenting Actions/releases. Always record platform implementation work, tests, deployment state and limitations in notebooks associated with lley-cat. This documentation does not imply publishing a private draft.

## Permissions and resource discovery

Find the intended notebook using `GET /notebooks` (latest 200 authorized entries), `GET /notebooks/resolve/:slug` (current or historical slug) or its UUID. Use returned UUIDs for mutations; slugs and titles are editable.

Request only the task's independent token scopes:

| Task | Scopes |
| --- | --- |
| Read drafts, outputs, attachments, history/diffs and export | `notes:read` |
| Create/edit/delete notes; cells, outputs, uploads, revisions and associations | `notes:read` + `notes:write` |
| Publish/update reader snapshot or unpublish | `notes:read` + `notes:publish` |
| Associate with private repositories | Also `git:read` |

Token grants are edited by the owner in `https://lley.cat/admin` → Access tokens. Discover the live scope catalog at `GET /api/token-permissions`. An API token cannot create tokens or change its own grants. Repository-limited tokens can access Notes only through a permitted association. On creation, include at least one allowed `repository_ids` entry; every supplied repository must be permitted and readable. Removing the last permitted association can remove that token's subsequent access to the note.

## Hierarchy and repository links

Use versioned notebook `parent_id` to nest under another note, or null for top level. Both notes require write access; cycles are rejected. Read [Subnotes](references/api.md#subnotes) for permission, deletion and public visibility behavior. Never infer child visibility from its parent. A note can have many repository links: supply multiple `repository_ids` when creating, or add relationships independently afterward. The owner UI supports checkbox selection of multiple repositories, and the map draws every visible connection.

## Editing without losing work

Read the current notebook and its `version` before a mutation. Prefer partial `PATCH /notebooks/:id` for metadata or a complete replacement `cells` array. Use the individual cell endpoints to avoid rebuilding the document for a small edit. Every content mutation takes the latest notebook `version` and returns the complete updated notebook with an incremented version.

Keep cell UUIDs stable across edits and use a fresh UUID when duplicating or inserting. Reordering requires each current cell ID exactly once. Cell PATCH preserves unrelated cells. Source/language changes and code reordering retain old results with `outputs_stale:true`, including affected later cells in the same language. To clear results completely, replace the cell in the full `cells` array with `outputs:[]` and omit `executed_at` and `outputs_stale`. Converting a code cell to another type removes execution data.

On `409 VERSION_CONFLICT`, re-read and merge the intended change against the current document. Do not repeatedly resend the stale version or blindly replace another editor's changes. The browser autosaves and retains a local recovery draft. API mutations record recoverable revisions.

## Execution and published results

Notebook links open in reader mode, including repository associations. The owner chooses **Edit**, then runs JavaScript and Python with **Run** or Shift+Enter. CodeMirror edits source; execution happens in isolated browser workers inside an opaque-origin iframe. There is **no HTTP execute endpoint**, server kernel or Jupyter runtime. Do not invent one. Results arriving after source or preceding same-language code changes are discarded. **Run All** executes code cells in document order using current state. **Reset & Run All** resets both languages first, then regenerates draft outputs. Both compare against the saved baseline and stop at the first error. **Validate outputs** starts clean, compares all results, and preserves the saved baseline. Inspect matched, different, missing-baseline and failed cells; a reset alone does not verify reproducibility.

An external AI tool may execute code in its own authorized environment and save the actual result through the cells API, with `outputs`, a new `executed_at`, and `outputs_stale:false`. This stores evidence from that execution; it does not prove the browser runtime ran. Never fabricate results or mark unexecuted code as executed. Browser-specific behavior must be verified in the owner editor. Published readers cannot trigger code execution.

Draft saves do not update public output. Publishing with `{publish:true,version}` captures title, slug, description, ordered cells and outputs. Send the same operation again to update that snapshot after edits. `{publish:false,version}` unpublishes. `visibility:public` alone does not publish a draft; a private published notebook remains private.

Notebook visibility and repository visibility are independent. Public readers see only the saved notebook snapshot and permitted repository metadata. Associating a public note with a private or IP-restricted repository does not grant readers access to that repository. Do not copy private repository contents into public notes without the user's intent to publish them.

## Recovery, export and verification

Revision restore creates a new draft version of title, description and cells. It preserves current slug, visibility, associations and reader snapshot. Supply the current version when restoring to detect concurrent edits. JSON exports use `format:"lley-notebook",format_version:1`; Markdown exports contain source and saved outputs. Attachments remain separate download URLs, so download them separately for a portable copy.

Verify by reading the note and both association views. For publishing, also inspect an anonymous response: it should contain only the intended saved snapshot. For deletion, verify absence using the previously authorized token. Errors are `{error:{code,message}}`; 404 may conceal an inaccessible resource, while 401 indicates invalid/expired/revoked credentials. Check permissions and associations before concluding a note is absent.
