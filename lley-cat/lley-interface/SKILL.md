---
name: lley-interface
description: Maintain the shared lley.cat, git.lley.cat and notes.lley.cat interface using its semantic design tokens, Workspace-derived navigation, themes, cards, editors and native interaction contracts.
---

# lley.cat Interface

Use the lley-cat repository's [design-system contract](https://git.lley.cat/r/cf7b2b43-ffd8-4fb7-9381-43a9246c4210?path=docs%2FDESIGN-SYSTEM.md). Workspace geometry and components derive from Dyadic; the later warm black/gold direction uses Ward as a color reference. Current Lley semantic tokens are authoritative, including separate Light, Dark and OLED roles. Do not restore an older navy palette or copy a different application's current palette over them. Other repositories are read-only unless separately authorized; an older local checkout may be stale. Preserve real platform capabilities and authored content.

The authoritative shared files are `src/theme-tokens.css`, `src/design-system.css`, `src/icons.tsx`, the upstream `*-primitives.css` files, `WorkspaceShell.tsx`, `WorkspaceSearch.tsx`, `Library.tsx`, `PopupMenu.tsx`, `ui.tsx` and `shared/ui/motion.mjs`. `app-layout.css` holds domain structure. Reuse these components for equivalent elements; do not create a parallel repository/note card or local control palette. Fonts are actual Geist/Geist Mono. Dark, Light and OLED use complete semantic roles, including code, diffs, charts, statuses, borders and focus. System follows this device. Preserve brands, actual branch names and authored titles/code.

Use normal English title case for controls and settings, with internal minor words lowercase. Full-width surfaces contain buffered content using `clamp(1rem, 4vw, 3rem)`; constrain the content pane, not the background. Source breakpoints are phone ≤780px, tablet 781–1100px and desktop ≥1101px; Settings sheets use 600px. The desktop rail is 68px and sidebar 264px. Search opens the Workspace search dialog through its icon or Ctrl/Cmd+K. Settings preserves the underlying page and returns there on close; Back closes the deepest overlay first.

Repository headers keep a compact clone field beside the title at the top-right. Updated/test status is directly left of Star, Upload, Download and Settings; no Refresh, ZIP text, duplicate branch selector or separate clone/upload toolbar. Repository navigation fills one row, retains icons and centered chevrons, and uses bounded popups with keyboard navigation. Repositories and Notes share heading/search/filter and entry geometry: Add at the title's upper right, All/Starred beside Search, stars and actual available test badges at entry top-right. Associated notes reuse the same entry component. Never fabricate tests or show badges for repositories without tests/Actions.

Note links open reader mode. Parent entry backgrounds expand children; title links navigate. No empty Subnotes bar. Tables scroll horizontally; Wrap Long Lines applies to code/source/diffs. Image previews retain pan, pinch/zoom, fit and Back dismissal. CodeMirror appearance changes must preserve edits, selection, cells and the isolated runtime environment. Save controls float bottom-right only for actual pending edits, disappear on revert/save, and retain autosave/version conflict handling.

Validate rendered phone, tablet and desktop pages in every theme against the current reference. Inspect all page types, menus, sheets, search, copy fields and controls; a passing build or matching hex values is insufficient. Test edit/revert/save, overlay return paths, narrow-screen overflow, runtime/output formatting and Android Back where affected. Use private disposable fixtures without changing authored notes or repository metadata. Document implementation, observed validation, deployment and limitations in a connected lley-cat notebook. Manual app deployment preserves volumes and does not activate delivery.

Owner appearance uses session-only `GET/PUT /api/preferences` with `appearance: system|light|dark|oled`; PATs cannot access account preferences. The validated non-secret appearance and wrap cookies synchronize the three domains. Android's trusted `theme` action updates native canvas/system-bar contrast without additional permissions. Native changes require a newly signed version/build with the existing signing identity; see [lley-android](../lley-android/SKILL.md).

## Shared Tracking, Search and Long Sheets

Reuse `Tracking.tsx` and `shared/tracking.mjs` for issue/PR/Notes categories, severity, workflow states, filters and sorting. Keep Draft/Published independent. Semantic `--track-*` roles give all nine sub-states separate Light and Dark/OLED colors; accompany color with readable text/dots. Custom categories must remain usable in lists and editors.

Repository and workspace content search must expose actual source matches with paths, line links and coverage. Use the shared search fields, keep folder controls usable on narrow screens, and inset results within full-width surfaces. Preserve selected refs and link matches to immutable commits.

`Modal` owns the fixed title/drag handle and a bounded `modal-scroll` region with native vertical scrolling. Elastic decoration must not remove the body's scroll container. Body gestures scroll results; header gestures dismiss the sheet. Verify long test reports to the last case, background-scroll containment, keyboard focus/Back, and mobile/tablet/desktop geometry across themes. Record observable UI results separately from unit, build, CI or physical-device evidence.
