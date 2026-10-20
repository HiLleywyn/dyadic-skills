---
name: lley-dyadic-embed
description: Integrate the portable lley.cat Git and rich Notes backend and React views into a host application such as Dyadic, using the separate integration branch and host identity, workspace permissions and vault credentials.
---

# Embed Git And Notes

The package is in `integrations/dyadic-platform/` on lley-cat branch `integration/dyadic-platform-scaffold`, deliberately separate from main. Read its [README](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?ref=integration%2Fdyadic-platform-scaffold&path=integrations%2Fdyadic-platform%2FREADME.md) before integration. Copy that folder or use its installable package; do not merge the entire application into the host.

Import `/server` only on the backend, `/react` and `/theme.css` in the browser, `/contracts` for typed schemas. Provide the host's real `authenticate`, `authorize`, `created`, `provider` and exact `origins`. Authentication returns the actual subject/workspace; authorization must consult workspace resource bindings and roles. The source PAT's capabilities never grant a host user access by themselves. The mapping migration is a template requiring actual host identity/role integration.

Keep source PATs in the host vault. `createLleyProvider` reads a credential per request and refuses redirects. The browser uses same-origin host cookies and never receives that PAT. Cross-workspace linked resources must remain filtered, including parents and attachments. Use repository-limited tokens where possible; repository provisioning needs an explicitly privileged flow. Never put one unrestricted owner credential behind an allow-all policy.

Notes stay independent from Git with many-to-many associations. Preserve stable cell UUIDs and require the current version for every edit. On a conflict, preserve the draft, load the new version and merge. Draft saves do not publish reader snapshots. Saved outputs require real execution. Runtime controls appear only with an injected isolated JavaScript/Python adapter; there is no MCP/server execute endpoint. See lley-notes for the full custom cell schema and runtime semantics.

Run `npm ci`, `npm test`, then `npm pack` inside the package. Test host authentication, tenant/resource denial, source permissions, actual notes conflicts and browser rendering in the target host before deployment. The package is a functioning remote-provider scaffold, not a completed installation in Dyadic; local Forgejo/Postgres provider migration, host vault/identity binding and richer host UI remain integration work. Do not claim those are deployed until verified.

The user has prohibited editing Dyadic during this task. Work only in lley-cat's integration branch and the private skills repository unless they later authorize host changes. Keep production delivery limited to the authorized lley-cat main verification; do not run this scaffold as a production deployment.
