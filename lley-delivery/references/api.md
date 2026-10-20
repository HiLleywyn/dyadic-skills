# Delivery API and stage format

Base: `https://git.lley.cat/api`. Authenticate with `Authorization: Bearer $LLEY_TOKEN`. Use stable repository UUIDs. HTTP failures use `{error:{code,message}}`; paused operations return `409 DELIVERY_PAUSED`.

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/repositories/:id/actions` | Configuration, optimistic version, pause, image allowlist, latest 50 runs |
| PUT | `/repositories/:id/actions` | `{version,config}`; `actions:write` |
| POST | `/repositories/:id/actions/preview` | `{config}`; validate graph and return ordered waves; no execution |
| POST | `/repositories/:id/actions/runs` | `{ref}`; requires `actions:run`, global delivery active and manual trigger enabled |
| GET | `/actions/runs/:id?after=0` | Run, stage results, up to 2000 log chunks after sequence, assets |
| POST | `/actions/runs/:id/cancel` | Cancel queued/running job |
| POST | `/actions/runs/:id/retry` | Create new run of the original immutable commit |
| GET/POST | `/repositories/:id/releases` | List or create release |
| GET/PATCH/DELETE | `/releases/:id` | Read, edit, delete release |
| POST | `/releases/:id/assets` | Multipart `file`, max 256 MB; returns UUID, bytes and SHA-256 |
| GET/DELETE | `/delivery/assets/:id` | Authorized attachment download or removal |
| GET/PATCH | `/delivery` | Owner session only; global pause, allowed images and runner status |
| POST | `/delivery/runners` | Owner `{name}`; one-time runner key |
| DELETE | `/delivery/runners/:id` | Owner revokes runner immediately |

The current safety requirement prohibits calling resume/run/retry or enabling any trigger on production without new owner authorization.

```json
{
  "version":1,
  "name":"Source checks",
  "triggers":{"push":false,"tags":false,"manual":false},
  "stages":[{
    "id":"verify","label":"Verify source","needs":[],
    "image":"node:24-bookworm-slim",
    "commands":[["node","--test","tests/example.test.mjs"]],
    "timeout_seconds":600,"memory_mb":512,"cpus":1,
    "artifacts":["results.json"]
  }]
}
```

IDs: lowercase letters/digits/hyphens, begin with a letter, max 48 characters. At most 30 stages; dependency graph must be acyclic. Image must match the gateway's allowlist. Limits: 1–3600 seconds, 64–4096 MB, 0.25–4 CPUs. Commands are arrays, not interpolated shell strings. Paths are explicit relative files/directories without traversal, `.git` or backslashes. Artifact symlinks are refused. Jobs have no network, host files or app credentials. Trigger monitoring reconciles real Git branches/tags approximately every 15 seconds; first observation establishes a baseline.

Create a release with `{version,title,body?,channel?,ref}`; channel is stable/beta/nightly. Initial state is draft. Source commit remains fixed. PATCH accepts `{title?,body?,channel?,status?}`, with draft/published status. Readers see only published releases except authorized owner/write access. Upload assets before publishing. Check returned `sha256` against a local hash. Asset downloads use stable UUIDs and remain gated by repository visibility/IP/token rules.

Runner protocol is private trusted-host infrastructure, not a normal AI client API. Register through the owner UI and use `ops/delivery-runner.mjs`; do not send runner keys to stage commands. Runs claim via leases, heartbeat and submit logs/results/assets. Keep all keys outside the repo.
