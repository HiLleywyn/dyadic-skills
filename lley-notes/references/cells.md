# Cell format and execution

## Contents

- [Document shape](#document-shape)
- [Cell types](#cell-types)
- [Output types](#output-types)
- [JavaScript](#javascript)
- [Python](#python)
- [Execution boundaries](#execution-boundaries)
- [Attachments](#attachments)

## Document shape

A notebook response contains `id,title,slug,description,visibility,status,cells,version,created_at,updated_at,repositories,editable,parent_id,parent,size_bytes`. `repositories` contains only repositories readable by the caller. `editable` reflects notebook write permission; the browser additionally requires the owner session to show editing controls. Timestamps are ISO instants; the UI presents local 24-hour time including seconds.

Each cell requires a real unique UUID, `type`, and string `source`. Optional fields are `language`, `outputs`, `executed_at` and boolean `outputs_stale`. Example:

```json
{"id":"48ce4f0f-ac35-42b5-a297-70397e7f934f","type":"code","language":"python","source":"sum(range(10))","outputs":[{"kind":"json","data":45}],"executed_at":"2026-10-19T15:10:20Z"}
```

This is a schema example, not evidence that the code ran. Preserve real outputs only after execution. API limits: 500 cells/notebook, 500,000 source characters/cell, 30 outputs/cell, 12 MB JSON request. Code languages are exactly `javascript` and `python`; JavaScript is the default if omitted.

## Cell types

| `type` | `source` | Rendering |
| --- | --- | --- |
| `markdown` | Markdown string | Sanitized Markdown; fenced code is highlighted |
| `heading` | Plain section heading | Second-level heading |
| `code` | Source code; set `language` | CodeMirror editor or highlighted reader code, then saved outputs |
| `math` | LaTeX expression without `$$` delimiters | KaTeX display math; trusted commands disabled |
| `table` | JSON array encoded **as a string** | Rows or object records; up to 500 rendered rows |
| `image` | `/media/ATTACHMENT_UUID` | An uploaded raster image |
| `attachment` | JSON object encoded **as a string**: `{"url":"/media/UUID","filename":"data.csv"}` | Download link |

Object-record table example: `source: JSON.stringify([{method:"A",score:0.9},{method:"B",score:0.8}])`. Array rows such as `[["Column","Value"],["A",1]]` also work; an all-string first row becomes the column header. Tables, including Markdown and execution outputs, preserve single-line values and scroll horizontally. Numeric display uses up to eight significant digits; hover the value for full precision, which is also preserved in exports. Markdown HTML is sanitized; iframe, form, style and executable output are not supported. Use a separate `math` cell for mathematical expressions.

## Output types

An output is `{kind,data}`, where `data` must be JSON serializable. There is no HTML output type.

| `kind` | `data` |
| --- | --- |
| `text` | Text, or a value rendered as formatted JSON |
| `error` | Error or traceback string |
| `json` | JSON scalar, array or object |
| `table` | Array of rows or object records |
| `image` | `data:image/png;base64,...`, `data:image/jpeg;base64,...` or `data:image/webp;base64,...` |
| `chart` | Numeric array, or `[{label:"A",value:3},{label:"B",value:5}]` |

Charts render as horizontal bar charts with full labels, a scale derived from the actual values, and an accessible data table; this is not a Vega, Plotly or arbitrary SVG/HTML renderer. Image output must be a supported base64 raster URL, not an arbitrary remote URL. Use uploaded images in an `image` cell for attachments. Clicking or tapping an image opens a lightbox. On mobile/tablet, pinch with two fingers to zoom and drag with one finger to pan; Fit resets it. Desktop also supports zoom buttons, double-click, `+`/`-` and `0` to fit; Escape closes it. The shared viewer handles notebook attachments, Markdown images, raster cell outputs and repository Markdown images.

## JavaScript

The last top-level expression produces a result. Top-level `await` works. Top-level variables/functions/classes persist across cells in the same JavaScript worker until reset. Use ordinary script syntax; module `import`/`export` is not supported by this cell runner.

```javascript
const records = [{label: 'A', value: 3}, {label: 'B', value: 5}];
console.log('Computed', records.length, 'rows');
console.table(records);
display(records, 'table');
chart(records);
records.reduce((sum, row) => sum + row.value, 0)
```

`console.log/info/warn` produce text; `console.error` produces error output. `display(value,kind='json')` accepts text/json/table/image/chart. `chart(values)` is shorthand for chart output. This example intentionally demonstrates several output mechanisms; use only the ones relevant to the document.

## Python

Python uses the locally served Pyodide runtime, with its standard library. Scientific packages such as NumPy, pandas and Matplotlib are not bundled. Do not rely on pip, micropip or fetching packages. Python globals persist across Python cells, separately from JavaScript globals.

```python
records = [{"label": "A", "value": 3}, {"label": "B", "value": 5}]
print("Computed", len(records), "rows")
display(records, "table")
chart(records)
sum(row["value"] for row in records)
```

`print` becomes text output; exceptions become traceback/error output. `display(value,kind="json")` and `chart(value)` are installed helpers. Return JSON-friendly Python lists, dictionaries and scalars for structured output.

## Execution boundaries

- Owner editor: Run or Shift+Enter for a selected code cell; Ctrl/Cmd+S saves.
- Run All executes code cells in document order with existing language state. Reset & Run All first resets both workers, then regenerates draft results. Stop interrupts the batch; the first error also stops it.
- Validate outputs resets both workers and executes in order without replacing saved results. Its report compares exact typed values (object key order ignored), text, arrays, tables, charts and image bytes. Dynamic timestamps, randomness, float differences and byte-level image changes may differ. Errors fail validation; a cell without saved output/execution metadata is reported as lacking a baseline, never as matched.
- Source/language changes and structural code edits mark affected same-language results stale. Old output remains visible with a warning, including after reload and API edits. Reset alone leaves saved output intact and does not certify it. Run again to regenerate; validation alone leaves stale flags unchanged because it preserves the baseline. Code/order changes during a batch discard the in-flight result and stop later execution.
- Per-language execution is serial. JavaScript has a 10-second limit; Python 45 seconds including first runtime load.
- Stop/Reset terminates the worker and loses its language state. Reloading also loses runtime state; saved outputs remain.
- Workers have no DOM or application credentials. Runtime network access is constrained to local engine assets by CSP; application APIs and arbitrary internet requests are unavailable.
- Browser workers use browser CPU/memory; there is no server container or promised per-cell memory quota.
- Outputs are saved with draft cells. Publish explicitly to make selected output visible to readers.
- Execution does not read repository files automatically. Supply any required data through code or the external tool's authorized workflow.

## Attachments

Upload multipart `file`, `kind=attachment`, `note_id=NOTEBOOK_UUID` to `/api/uploads`. Limit 8 MiB. Images accept PNG/JPEG/WebP/GIF/AVIF, validate dimensions (25 million input pixels), remove metadata and are re-encoded as WebP. Additional downloads accept validated PDF, ZIP, UTF-8 TXT/MD/CSV and JSON. SVG and executable attachments are not supported.

Use the returned `url` exactly in the image/attachment cell. The API enforces the notebook's visibility for `/media/:id`. Anonymous access additionally requires that the published snapshot reference the attachment. Uploading alone does not publish it.

List attachment metadata with `GET /notebooks/:id/attachments`. Delete an unused upload with `DELETE /notebooks/:id/attachments/:attachment`. `409 ATTACHMENT_IN_USE` protects files referenced in a draft, published snapshot or revision history. Deleting a whole notebook removes its attachment storage and revisions. An export is not a self-contained attachment archive; download files separately and re-upload them when moving between installations.
