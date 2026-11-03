---
name: lley-delivery
description: Configure and inspect the custom lley.cat Actions, CI/CD stage graphs, isolated runners, logs, artifacts and Releases through git.lley.cat. Use for this platform's delivery system and release assets.
---

# lley.cat Actions and Releases

Use `https://git.lley.cat/api`, with the same owner-issued personal token used for Git and Notes. This is a custom stage graph and release service, not GitHub Actions or Forgejo Actions. Do not create `.github/workflows`, use marketplace actions, or call Forgejo `/api/v1` to manage delivery.

Read [API and stage format](references/api.md) before changing configuration, starting runs or publishing assets. Use [lley-git](../lley-git/SKILL.md) for source and repository management, [lley-notes](../lley-notes/SKILL.md) for connected work documentation and [lley-android](../lley-android/SKILL.md) for native builds.

## Activation and task scope

Inspect the target repository's current activation, triggers and the user's authorization for this task. An older Lley-only rollout was a session constraint, not a permanent prohibition on separately authorized Dyadic or Ward workflows. Preserve unrelated repository settings. The server has a separate repository activation gate in admission, ref reconciliation and runner claims. Global resume does not activate other repositories. Owner-only `POST /repositories/:id/actions/activation` controls that gate; normal tokens and MCP cannot activate it. Use manual triggering for controlled production verification. Preview validates without executing. Validate changes in disposable infrastructure before production runs; neither a skill nor a source push grants activation authority.

## Permissions

| Operation | Independent scope |
| --- | --- |
| Config, runs, logs and build artifact reads | `actions:read` |
| Edit stage graph and triggers | `actions:write` |
| Start, retry, cancel runs when delivery is enabled | `actions:run` |
| Read releases and their assets | `releases:read` |
| Create/edit/delete releases, publish/unpublish, upload/delete assets | `releases:write` |
| List credential metadata and protected environments | `secrets:read` |
| Set/rotate/delete write-only credentials; edit environment policy | `secrets:write` |

Repository restrictions apply. Add read grants when a script needs to inspect its changes. A write grant does not silently imply the read grant. Public/IP visibility allows appropriate anonymous reads; draft releases require release write permission. Global pause and runner registration require the owner browser session. PATs cannot mint runner credentials or resume global delivery.

## Configuration and execution

Read the repository's current configuration and optimistic `version`. Save both the new configuration and latest version with `PUT /repositories/:id/actions`. Re-read and merge a `409 CONFIG_CONFLICT`. `.lley/pipeline.json` is a source-controlled template; editing it alone does not replace the database configuration.

Commands are argv arrays in restricted containers. Use owner-prepared allowlisted images. Stages are offline by default; explicit `network.allow_hosts` enables HTTPS CONNECT only through a separate proxy that denies private/local/reserved destinations. Never add Docker sockets, host mounts or arbitrary host commands. The fixed `lley-app` deployment operation is bound specifically to lley-cat and explicit runner settings; it cannot receive arbitrary job credentials or become a host shell escape.

Read the repository's credential metadata before writing. `PUT /repositories/:id/secrets/:name` takes `{version,value,environment?,expires_at?}`; values are write-only and encrypted. Use the latest metadata version when replacing/deleting; `SECRET_CONFLICT` requires a reload. Never include values in pipeline JSON, commands, logs, notes or tool arguments unrelated to the credential write. Environment-specific names override repository-level names. A stage selects bindings with `secrets:{ENV_VAR:"STORED_NAME"}` and optional `environment`. Plain `variables` are visible in configuration and are not secrets. Reserved runtime/proxy names are rejected.

Protected environments allow exact refs or explicit trailing `/*` prefixes and may require approval for the immutable run. Only the owner session can approve. Stages receive selected values through stdin; Docker inspect/arguments do not contain them and job Docker logging is disabled. Logs are masked and recognizable credential bytes are blocked from artifacts. Do not claim masking defeats arbitrary transformation by malicious authorized job code. Revocation/rotation affects future access; it cannot erase a value already in a running process.

Declare `reports:[{path:"reports/unit.xml",format:"junit"}]` or `lley-json`. Collect real case results even when a command fails. Missing/malformed reports or failing cases fail the stage. Repository Tests and Action run details expose cases, durations and failures. Badges mark outdated commits and do not treat absent reports as success. Public/private/IP gates also protect badge URLs; never add a PAT to a badge URL. MCP `ci_*` tools expose the same contract without owner activation/approval tools.

Runs pin an immutable commit; retries create a new record. Cancellation is cooperative through bounded heartbeats and container termination. Leases expire; an expired job is failed rather than silently repeated. Inspect terminal status and actual logs/assets before claiming success. A configured pipeline, successful preview or published release is not evidence that a run executed.

## Releases and documentation

Create a draft pinned to an actual branch/tag/commit, upload real artifacts, verify returned size and SHA-256, then publish when the user's task authorizes publication. Release publication does not run Actions. Deleting a release removes its assets; confirm the exact release identity is within the user's requested scope.

Always keep implementation, validation, deployment status and limitations in notes associated with lley-cat when working on the platform. Preserve facts: distinguish browser/emulator tests from physical-device validation. Never save credentials or private signing material in notes or release bodies.


## Shared UI Rules

Use normal English title case in menus, settings, statuses and displayed test names; lowercase internal articles, conjunctions and prepositions. Preserve acronyms, authored content, actual code and branch/file identifiers. The persistent rule is in the lley-cat AGENTS.md. Reuse shared searches, dropdowns, rectangular status/count boxes and buffered full-width semantic surfaces from the current theme tokens. Tests has equal colored totals, a single 3:1 search/filter row and inward-indented stage/suite/case groups. Do not repeat selected-run metadata or add explanatory paragraphs to pages.

Badges display `Tests`, `Not Run`, `Passed`, `Outdated` and other title-cased colored labels. They are hidden when no Actions are configured, no run history exists and no recognized test source is present. Source presence can produce `Not Run`, never success. Report names/codes remain unchanged in the API; presentation casing is applied only by the UI.

All pages use the shared --content-gutter (Dyadic’s clamp(1rem, 4vw, 3rem)) inside full-width surface backgrounds. Apply it to real content rows as well as headings, including associated notes, notebook subnotes/execution, libraries, Settings, tests, actions and releases. Do not put header actions or toolbars outside their containing box. Verify actual geometry at mobile/tablet/desktop sizes and CSS specificity rather than assuming an outer selector covers every component.


Interface work follows [lley-interface](../lley-interface/SKILL.md): the current Lley semantic theme tokens, Workspace-derived geometry, Geist/Geist Mono, responsive rail/drawer, bounded menus and common cards/controls. Settings → Security contains Access Tokens. Preserve platform authorization and authored content while changing the UI.

## Tracking and Test/Build Gates

Use the shared tracking contract for issues or PRs the user authorized creating/updating: custom categories, evidence-backed severity, and Open/Closed sub-states. A failing test is not automatically a security vulnerability or Critical severity. Link relevant real run IDs and source commits.

For platform source changes, run `npm test`, `npm run check` and `npm run build`, plus the integration workflow relevant to the changed boundary. `npm run test:tracking` requires the explicitly isolated tracking fixture; do not redirect it to production. Then run the approved custom Actions pipeline at the exact immutable commit when the task calls for hosted checks. A local build or configuration preview does not count as hosted execution. Read actual per-case reports, artifacts and terminal stage results.

Long Action Run sheets must retain a dedicated vertical body scroller while the header supports dismissal. Verify that the final test cases are reachable on phones and that the background page does not move. Shared web changes reach the live-URL Android shell without an APK rebuild; native/bundled changes require the signed build, instrumentation/login and publication gates in [lley-android](../lley-android/SKILL.md). Preserve all unrelated repository activation settings.
