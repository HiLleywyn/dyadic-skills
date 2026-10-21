---
name: lley-profile
description: Manage the Lley.cat public profile, independent repository and note pins, contribution history and shared avatar navigation through the platform API or typed MCP tools.
---

# Lley.cat Profile

The public page is `https://lley.cat/profile`; Home contains the map/directory without the former profile rail. The shared header has the Home wordmark on the left and avatar menu on the right. Its sections are Home; Profile with indented Repositories and Notes; Settings. Profile opens the public page for the owner too. Editing identity is Settings → Profile; Access Tokens is inside Settings → Security.

Use the platform's typed MCP tools when connected. Otherwise use the three-domain `/api` with the existing scoped bearer credential kept in the client vault, never in source, a URL, command arguments or a notebook.

| Task | MCP | HTTP |
| --- | --- | --- |
| Read supplied identity/current project | `platform_profile_get` | `GET /profile` |
| Change supplied fields | `platform_profile_update` | `PATCH /profile` |
| Read visible pinned items | `platform_profile_pins_get` | `GET /profile/pins` |
| Replace pins | `platform_profile_pins_set` | `PUT /profile/pins` |
| Read real contributions and feed | `platform_profile_activity` | `GET /profile/activity` |

Profile edits and pins require global `profile:write`; no token is broadened automatically. PATCH preserves omitted fields even when the read response hides the current private project. PUT `/profile` remains a full profile replacement for the settings form. Never generate biography, links or repository descriptions that the user has not supplied.

Pins are distinct from owner stars. Read the current pins, then replace with `{items:[{kind:"repository",id:"UUID"},{kind:"note",id:"UUID"}]}` using stable IDs and at most twelve unique entries. Every entry must be readable. Preserve existing pins unless replacement is requested. Public readers receive only authorized pins; a public notebook association never exposes a private repository. Deleted resources remove their own pins. Editing pins does not edit repository/note contents.

Activity is **365 UTC days of actual visible self-hosted default-branch commits and notebook activity**, including AI-authored repository commits. It is not a claim of personal authorship or imported GitHub activity. Privileged readers see note creation/revisions; public readers see actual public publications and their published identity, never current draft changes. `partial:true` indicates unavailable/bounded Git history (100 repositories, 2,000 commits each); do not present that as a complete total. The feed contains the latest sixty entries. Missing history must not become fabricated events or green status.

Use normal English title case for controls, lowercase internal minor words, and preserve authored text/branch names. Place the profile avatar above the names at the upper left and the biography to their right. Website links and socials use separate centered horizontal rows below both columns. Absent/whitespace-only fields and empty rows must not render or reserve gaps; the graph scrolls within its own region on mobile. Public/privacy-sensitive behavior must be verified anonymously as well as with the owner; owner-warmed caches do not authorize other readers. Detailed contract and fixture evidence are in lley-cat `docs/PROFILE.md`. Document changes in the connected lley-cat work note using [lley-notes](../lley-notes/SKILL.md).

Profile Save floats at bottom-right only for pending edits; reverting hides it. Link settings use compact labeled rows with grouped reorder/remove controls and optional icon controls. Public website links and brand socials use separate compact centered rows; omit empty rows.


Interface work follows [lley-interface](../lley-interface/SKILL.md): the current Dyadic Workspace source, Geist/Geist Mono, shared Dark/Light/OLED roles, responsive rail/drawer, bounded menus and common cards/controls. Settings → Security contains Access Tokens. Preserve platform authorization and authored content while changing the UI.
