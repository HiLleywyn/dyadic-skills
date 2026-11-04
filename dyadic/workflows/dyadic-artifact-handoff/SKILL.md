---
name: dyadic-artifact-handoff
description: "Trace a Dyadic deliverable from generated output to retained bytes, exact revisions and a usable attachment or UI reference. Use when a file, image or panel is reported complete but is missing, stale or cannot be opened."
---

# Artifact Handoff

Start with the specific thing the user expected to receive: a downloadable file, an image in the conversation, or a persistent interactive panel. Those have different delivery paths. “The tool succeeded” establishes only that tool’s reported result.

For workspace files, inspect the actual path and supplied file/version receipts. Prefer the retained revision identified by the producing operation. Record the path, revision and hash when available; do not replace a missing historical body with today’s file. **Files and Checks** distinguishes downloadable attachments, retained workspace versions and failed packaging/sending attempts. Download availability does not prove a person downloaded the file.

For a generated image, separate generation, persistence, attachment/API delivery and rendered conversation visibility. A stored image ID or saved file does not establish the final two. Reuse the existing stored result when the requested repair is delivery; another generation changes the artifact and may incur another charge.

For declarative panels, `artifacts.read` returns the actual revision and current ready state. Read before a revision change and preserve stable component IDs. A structural validation or stored hash is not visual or semantic acceptance. Use the platform-provided UI reference; do not fabricate one from an artifact ID.

For archives, check the member manifest against the intended revisions and hashes. Packaging does not renew stale tests. If a stopped turn retained real output, report that partial delivery and the failed/missing step instead of treating cancellation as proof that nothing exists.

An owner’s interactive chat can use `runs.lookup` for an exact `iris:workspace:...` operation ID when available. A delegated specialist cannot use the owner-only recording reader; its parent must supply the relevant receipts and files. Keep those IDs out of file, chat and artifact namespaces.

Finish with what is available, how to open it, the exact version checked and the narrowest remaining delivery failure. Say when physical-device or rendered-UI behavior was not observed. Avoid replaying an uncertain generation or external send solely to get a cleaner success message.
