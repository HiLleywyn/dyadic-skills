# Notes API and recipes

Base: `https://notes.lley.cat/api`. Authenticate with `Authorization: Bearer $LLEY_TOKEN`. JSON mutations need `Content-Type: application/json`. Notebook mutations return the updated notebook, including its new `version`; use that value for the next operation.

## Contents

- [Notebook lifecycle](#notebook-lifecycle)
- [Cell operations](#cell-operations)
- [Publishing and recovery](#publishing-and-recovery)
- [Attachments and export](#attachments-and-export)
- [Repository associations](#repository-associations)

## Notebook lifecycle

| Method | Path | Input / behavior |
| --- | --- | --- |
| GET | `/notebooks` | Latest 200 authorized notebooks |
| POST | `/notebooks` | Create a draft; 201 |
| GET | `/notebooks/resolve/:slug` | Current or previous slug |
| GET | `/notebooks/:id` | Authorized draft or saved reader snapshot |
| PATCH | `/notebooks/:id` | `{version,...changedFields}`; fields: title, slug, description, visibility, cells |
| PUT | `/notebooks/:id` | Complete title, slug, description, visibility, cells and version |
| DELETE | `/notebooks/:id` | Delete notebook, revisions, associations and attachment storage |

Create JSON:

```json
{"title":"Experiment","slug":"experiment","description":"","visibility":"private","repository_ids":[],"cells":[]}
```

Title limit: 200 characters; description: 2,000; slug: 100, lowercase letters/digits with `.`, `_`, `-` separators. Slug aliases remain reserved after renaming. `repository_ids` is for creation only; use association endpoints afterward. A repository-restricted token must supply permitted repository IDs on creation. The title/description should be supplied or requested by the user.

For a description-only change, GET the note, then:

```json
{"version":7,"description":"Updated description supplied by the owner"}
```

PATCH does not accept `status`, `published`, timestamps, IDs or `repositories`. Publish through the separate endpoint. Associations are managed independently. PUT remains useful for an entire editor document or importing cell content from a JSON export; pass only editable fields and the current version, rather than assuming export metadata is writable. An API token with notes:read can inspect an authorized draft; an anonymous reader receives the saved published snapshot.

## Cell operations

| Method | Path | JSON body |
| --- | --- | --- |
| POST | `/notebooks/:id/cells` | `{version,cell,position?}`; zero-based position, append by default; 201 |
| PATCH | `/notebooks/:id/cells/:cell` | `{version,cell:{...changedCellFields}}` |
| DELETE | `/notebooks/:id/cells/:cell` | `{version}` |
| PUT | `/notebooks/:id/cells/order` | `{version,cell_ids:[...]}`; exact permutation of all current cell UUIDs |

All require `notes:write`. Responses are full notebooks, not isolated cells. Cell IDs are immutable on PATCH. Insertion rejects duplicate IDs. Whole-document saves also reject duplicate cell IDs. See [cell format](cells.md) for types and output data.

An example JavaScript client recipe, using an existing token and notebook ID:

```javascript
const base = 'https://notes.lley.cat/api';
async function call(path, method = 'GET', body) {
  const response = await fetch(base + path, {
    method,
    headers: {Authorization: `Bearer ${process.env.LLEY_TOKEN}`, 'Content-Type': 'application/json'},
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(`${response.status}: ${data.error.code}: ${data.error.message}`);
  return data;
}
let note = await call(`/notebooks/${process.env.NOTE_ID}`);
const cell = {id: crypto.randomUUID(), type: 'code', language: 'python', source: 'sum(range(10))'};
note = await call(`/notebooks/${note.id}/cells`, 'POST', {version: note.version, cell});
// Run in the owner editor, or execute independently in the tool's authorized runtime.
// Save only the actual observed output with a subsequent cell PATCH.
```

To save a real result, cell PATCH accepts `outputs:[{kind:"json",data:...}]` and `executed_at:new Date().toISOString()`. Editing source/type/language via cell PATCH removes old outputs/execution timestamp unless replacement outputs are included. Whole-document PUT/PATCH stores the cells as supplied, so clear stale results yourself when replacing a whole array.

If a mutation returns `409 VERSION_CONFLICT`, re-read, preserve other edits, and retry the intended change using the new version. Invalid reorder payloads return `400 INVALID_CELL_ORDER`. Omitted/invalid versions return 400. `404` can mean absent or outside token access; do not recover by creating a duplicate automatically.

## Publishing and recovery

| Method | Path | JSON / result |
| --- | --- | --- |
| POST | `/notebooks/:id/publish` | `{publish:true,version}` capture or update snapshot; false unpublish |
| GET | `/notebooks/:id/revisions` | Latest 100 previous `{version,created_at}` records; notes:write |
| POST | `/notebooks/:id/restore/:revisionVersion` | `{version:CURRENT_VERSION}` recommended; notes:write |

Publish requires the separate `notes:publish` scope. It captures current saved cells and outputs, not unsaved editor text. Editing a published notebook changes its draft while anonymous readers continue to see the previous snapshot. Updating its description or title does not update the reader snapshot until publishing again. Visibility changes take effect immediately; setting a published note private conceals it.

Restoring a revision makes a new version, preserves current slug/visibility/associations and leaves the reader snapshot unchanged. The old version remains recoverable. For compatibility, restore accepts an omitted body and checks the version observed at request start; send the current version explicitly for script concurrency control.

## Attachments and export

| Method | Path | Input / result |
| --- | --- | --- |
| POST | `/uploads` | Multipart `file`, `kind=attachment`, `note_id`; 201 `{id,url,filename?}` |
| GET | `/notebooks/:id/attachments` | Attachment metadata with `/media/:id` URLs; notes:write |
| DELETE | `/notebooks/:id/attachments/:attachment` | Delete an unreferenced upload; notes:write |
| GET | `/notebooks/:id/export` | Download `format:"lley-notebook",format_version:1` JSON, including authorized cells and output |
| GET | `/notebooks/:id/export?format=markdown` | Markdown download |

Attachment content is at `https://notes.lley.cat/media/:id`, outside `/api`, using the same token. Limits and cell encoding are in [Attachments](cells.md#attachments). `409 ATTACHMENT_IN_USE` means a current or recoverable version still refers to that file; do not bypass it. Whole notebook deletion removes files with its history.

## Repository associations

```json
{"repo_id":"REPOSITORY_UUID","note_id":"NOTEBOOK_UUID","position":0}
```

Send to `PUT /associations` to add or reorder. Remove with `DELETE /associations/:repo/:note`. Both require notebook write access, repository read access and a permitted repository restriction. Associations do not increment the notebook content version. The notebook `repositories` and repository `notes` views reflect the same many-to-many records.

For GitHub, create or find a local GitHub reference using the Git skill, then associate its **local UUID**. Do not submit a GitHub URL where a UUID is expected. The local repository page shows the Notes section; this cannot add UI to GitHub's own website.
