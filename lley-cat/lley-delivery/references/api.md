# Actions and Releases API

Base `/api` on all three lley.cat domains. JSON failures use `{error:{code,message}}`. Tokens issued in Settings → Security → Access Tokens work here; grants are independent and repository restrictions apply. Grants: `actions:read`, `actions:write`, `actions:run`, `releases:read`, `releases:write`, `secrets:read`, `secrets:write`, `stars:read`, `stars:write`. Existing grants are never broadened automatically. [Typed MCP tools](../../lley-mcp/SKILL.md) use the same authorization.

Public and allowed-IP readers can inspect public Actions and published releases without authentication. Private resources need the relevant read grant. Draft release access requires the owner or `releases:write`. Mutation grants apply separately. Owner session is required for global delivery and runner registration; normal API tokens cannot resume delivery or register a runner.

| Method | Path | Input / response |
| --- | --- | --- |
| GET | `/repositories/:id/actions` | `{version,config,updated_at,paused,images,runs}` |
| PUT | `/repositories/:id/actions` | `{version,config}`; returns incremented version |
| POST | `/repositories/:id/actions/preview` | `{config}` → `{waves,stages,network,paused}`; no execution |
| POST | `/repositories/:id/actions/runs` | `{ref}` → 201 immutable run; paused → `409 DELIVERY_PAUSED` |
| GET | `/actions/runs/:id?after=sequence` | Run, stage results, latest 2000 log chunks after sequence, assets |
| POST | `/actions/runs/:id/cancel` | Cancel queued/running run |
| POST | `/actions/runs/:id/retry` | New run of original immutable commit |
| GET | `/repositories/:id/releases` | Visible releases and assets |
| POST | `/repositories/:id/releases` | `{version,title,body?,channel?,ref}` → 201 draft |
| GET | `/releases/:id` | Release and assets |
| PATCH | `/releases/:id` | `{title?,body?,channel?,status?}` |
| DELETE | `/releases/:id` | Delete record and its assets |
| POST | `/releases/:id/assets` | Multipart field `file`, max 256 MB → 201 `{id,name,size,sha256,...}` |
| GET | `/delivery/assets/:id` | Stream authorized attachment |
| DELETE | `/delivery/assets/:id` | Remove asset with write grant |
| GET | `/delivery` | Owner global status, images and redacted runner metadata |
| PATCH | `/delivery` | Owner `{paused:boolean}`; pausing cancels running jobs |
| POST | `/delivery/runners` | Owner `{name}` → one-time `{id,name,key}` |
| DELETE | `/delivery/runners/:id` | Owner revokes runner and cancels its active job |
| GET | `/activity` | Owner-only latest completed run / published release events for native notifications |

`config` is format version 1 with `name`, `triggers:{push,tags,manual}`, `stages`. Example: [.lley/pipeline.json](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?path=.lley%2Fpipeline.json). Limits: 30 stages, unique lowercase identifiers up to 48 characters, acyclic `needs`, allowlisted images, argv commands, 1–3600s timeout, 64–4096 MB, 0.25–4 CPUs, explicit relative artifact paths. Stages can declare selected credential bindings, plain variables, an environment, report paths and exact HTTPS destinations as described below. Host bind mounts, privileged settings and Docker sockets are not job capabilities. Unknown keys and invalid resources/paths are rejected. Only lley-cat may use the configured `deploy:"lley-app"` target; host deployment uses fixed local configuration and does not accept arbitrary credential/egress/report fields. `409 CONFIG_CONFLICT` means re-read the current configuration and merge.

All triggers and repository activation are disabled on first use. Global pause is another server-enforced barrier. Inspect current task authorization and activation rather than reusing historical rollout restrictions or enabling additional repositories implicitly. `POST /repositories/:id/actions/activation` with owner `{enabled:boolean}` changes the separate repository gate. A normal token or MCP cannot activate it. Even manual starts/retries require global resume, repository activation and their enabled trigger. Reconciliation observes actual Git refs every 15 seconds when enabled and establishes a baseline without replaying history. Runs pin a commit before queuing; cancellation, stage failure and expired leases have explicit terminal states.

Releases pin `commit_sha`; editing a release never moves its source. Channels are stable/beta/nightly; status is draft/published. Upload real files, verify the returned SHA-256, then PATCH `{status:"published"}`. Publishing does not activate or enqueue Actions. File responses use attachment disposition, `nosniff` and the existing repository/IP gate.

The trusted runner protocol uses `X-Lley-Runner` and per-run `X-Lley-Lease`; keys are hashed in the database and never exposed to normal reads. `POST /runner/claim`, `POST /runner/runs/:id/heartbeat`, `GET /runner/runs/:id/source`, and POST `logs`, `results`, `assets` are for `ops/delivery-runner.mjs` only. Leases last 90 seconds with 15-second heartbeats. Revocation blocks new access. Runner credentials never enter job containers.

## Credentials and environments

| Method | Path | Contract |
| --- | --- | --- |
| GET | `/repositories/:id/secrets` | `secrets:read` → `{configured,secrets,environments}`; metadata only |
| PUT | `/repositories/:id/secrets/:name` | `secrets:write`; `{version,value,environment?:"",expires_at?:null}`; version 0 creates, latest version replaces |
| DELETE | `/repositories/:id/secrets/:name` | `secrets:write`; `{version,environment?:""}`; optimistic delete |
| PUT | `/repositories/:id/environments/:name` | `secrets:write`; `{version,require_approval,allowed_refs}` |
| DELETE | `/repositories/:id/environments/:name` | `secrets:write`; remove its credentials first |
| POST | `/actions/runs/:id/approvals/:environment` | Owner approves this running immutable job; cannot be called with a PAT |
| POST | `/runner/runs/:id/stages/:stage/credentials` | Valid lease + ready dependencies + activation/ref/approval checks; returns `{waiting:true,environment}` or selected values to the trusted runner |

Names are uppercase letters/digits/underscores, starting with a letter, maximum 64 characters. Values are 8–65536 characters. Environment identifiers are lowercase slug identifiers, up to 48 characters. Metadata contains name, scope, revision, creation/update, expiry and last use; it never contains the verifier/ciphertext/value. At rest, AES-256-GCM uses a separate private 32-byte `delivery_key` Docker secret and repository/environment/name context. Keep the key with encrypted backup configuration; losing it loses credential decryption and historical log masking. API rotation is replacing a named value with its latest version. Conflicts return `SECRET_CONFLICT` / `ENVIRONMENT_CONFLICT`.

Stage extensions:

```json
{
  "environment": "production",
  "secrets": { "DEPLOY_TOKEN": "PROVIDER_TOKEN" },
  "variables": { "RELEASE_CHANNEL": "stable" },
  "network": { "allow_hosts": ["api.example.com"] },
  "reports": [{ "path": "reports/unit.xml", "format": "junit" }]
}
```

Environment-specific values override repository names; missing/expired values fail closed. `allowed_refs` uses exact branches/full refs or an explicit trailing `/*` prefix. Tags require full `refs/tags/…` entries. Approval applies to this run, not a blanket future grant. Plain variables are readable configuration. Runtime/proxy variables are reserved. Values reach jobs over stdin rather than Docker arguments or Docker environment metadata. Logs are masked before upload and again by the server; encrypted per-run snapshots preserve masking across later rotation. Recognizable credential bytes block artifacts. Deliberately transformed output from malicious authorized code is outside a masking guarantee.

Jobs are offline by default. A stage with explicit hosts gets a dedicated internal network and separate HTTPS CONNECT proxy. The proxy resolves and rejects non-public IPs, allows port 443 only, exposes no host port and receives no credential. It does not decrypt allowed TLS traffic. Containers keep their CPU/memory/time/PID limits and lack host mounts, credentials and Docker sockets except the specifically bound values in their own process environment. All per-stage resources are cleaned up.

## Tests, badges and stars

`GET /repositories/:id/tests` returns the default branch's latest run/history, real case totals, head commit and status. Status includes `not-run`, queued/running/cancelled, failed/passed, `stale` for an old commit and `unverified` when source freshness cannot be established. `GET /repositories/:id/badges/tests.svg` returns an SVG under the same repository/IP gate with `private,no-store` caching. Do not put a token in its URL.

`GET /actions/runs/:id` includes `test_reports:[{stage,path,report,created_at}]` and approvals. Reports contain totals, duration and individual `{name,suite,status,duration_ms,message,file?,line?}` cases. `POST /runner/runs/:id/tests` takes `{stage,path,source}` for a declared report under a live lease. JUnit XML forbids DTD/entity declarations; both formats are bounded to 2 MB and 10,000 cases per report. Missing/malformed declared reports or failed/error cases prevent run success, even after exit code zero. `lley-json` is `{version:1,cases:[...]}`; case statuses are passed/failed/error/skipped.

`GET/PUT/DELETE /repositories/:id/star` reads or changes the owner's favorite, using `stars:read` / `stars:write`. `GET /stars` lists readable favorites within token repository restrictions. Anonymous visitors cannot inspect or mutate owner favorites. No visitor registration or community counts are added.
