---
name: lley-delivery
description: Configure and inspect the custom lley.cat Actions, CI/CD stage graphs, isolated runners, logs, artifacts and Releases through git.lley.cat. Use for this platform's delivery system and release assets.
---

# Lley.cat Actions and Releases

Use `https://git.lley.cat/api`, with the same owner-issued personal token used for Git and Notes. This is a custom stage graph and release service, not GitHub Actions or Forgejo Actions. Do not create `.github/workflows`, use marketplace actions, or call Forgejo `/api/v1` to manage delivery.

Read [API and stage format](references/api.md) before changing configuration, starting runs or publishing assets. Use [lley-git](../lley-git/SKILL.md) for source and repository management, [lley-notes](../lley-notes/SKILL.md) for connected work documentation and [lley-android](../lley-android/SKILL.md) for native builds.

## Current activation constraint

The owner has explicitly required all Actions/CI/CD triggers to remain disabled and the production delivery queue paused until separately authorized. Do not resume delivery, enable manual/push/tag triggers, start or retry a run as part of configuration, installation, testing, publishing a release or pushing source. Preview validates the graph without executing it. Verify production safety from `GET /repositories/:id/actions`: `paused:true` and all `config.triggers` false. Test actual execution against the disposable database workflow in the lley-cat repository, never by temporarily resuming production.

## Permissions

| Operation | Independent scope |
| --- | --- |
| Config, runs, logs and build artifact reads | `actions:read` |
| Edit stage graph and triggers | `actions:write` |
| Start, retry, cancel runs when delivery is enabled | `actions:run` |
| Read releases and their assets | `releases:read` |
| Create/edit/delete releases, publish/unpublish, upload/delete assets | `releases:write` |

Repository restrictions apply. Add read grants when a script needs to inspect its changes. A write grant does not silently imply the read grant. Public/IP visibility allows appropriate anonymous reads; draft releases require release write permission. Global pause and runner registration require the owner browser session. PATs cannot mint runner credentials or resume global delivery.

## Configuration and execution

Read the repository's current configuration and optimistic `version`. Save both the new configuration and latest version with `PUT /repositories/:id/actions`. Re-read and merge a `409 CONFIG_CONFLICT`. `.lley/pipeline.json` is a source-controlled template; editing it alone does not replace the database configuration.

Commands are argv arrays executed only in containers, with no network or credentials. Use owner-prepared allowlisted toolchain images for dependencies. Do not add tokens, signing keys, Docker sockets, host mounts or arbitrary host commands. The `lley-app` deployment type is a trusted host operation bound specifically to lley-cat and explicit runner settings. It is not a generic shell escape.

Runs pin an immutable commit; retries create a new record. Cancellation is cooperative through bounded heartbeats and container termination. Leases expire; an expired job is failed rather than silently repeated. Inspect terminal status and actual logs/assets before claiming success. A configured pipeline, successful preview or published release is not evidence that a run executed.

## Releases and documentation

Create a draft pinned to an actual branch/tag/commit, upload real artifacts, verify returned size and SHA-256, then publish when the user's task authorizes publication. Release publication does not run Actions. Deleting a release removes its assets; confirm the exact release identity is within the user's requested scope.

Always keep implementation, validation, deployment status and limitations in notes associated with lley-cat when working on the platform. Preserve facts: distinguish browser/emulator tests from physical-device validation. Never save credentials or private signing material in notes or release bodies.
