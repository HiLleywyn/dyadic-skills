---
name: dyadic-current-work
description: "Revise accepted work in Dyadic while preserving the owner’s constraints, exact file versions and unresolved items. Use for a follow-up that changes an accepted delivery or needs a Patch against it."
---

# Current Work Revision

Use the accepted brief as the baseline for the requested change, not as general memory. Acceptance belongs to the owner through **Accept Work**; an agent saying “accepted” does not create that state.

Read the available Current Work context and identify the accepted file revision IDs, constraints and unresolved items. If the brief was not supplied to this agent, ask the parent for that specific context. Do not invent a tool for reading it or reconstruct an acceptance from conversational praise. A supplied report of acceptance is weaker than the native saved record.

Compare the requested delta with that baseline. Separate constraints the owner changed from those that still hold. Read the affected files before proposing edits; flag intervening owner edits and missing dependencies. A matching filename or matching bytes at a later revision does not make an old verification current.

For a patch, discover the actual workspace tool schemas. `workspace.patch_preview` and `workspace.files` must use the same patch and base versions. If the base changes, prepare a new preview. **Change Requirement** opens Dyadic’s existing Patch review; it does not authorize every suggested edit. Account permissions and existing execution approvals still apply.

Bind the handoff to the resulting file revisions and the checks that actually used them. Report the changed requirement, preserved constraints, unresolved conflicts and any stale checks. Treat input-file presence as an input receipt, not proof that a test asserted every requirement. The owner can accept the revised answer with its exact updated versions.

Current Work is conversation-scoped. Temporary conversations cannot retain it; moving work to a different project/library needs review there. Its initial limits are 20 ordinary files totaling 8 MB, a 1,200-character brief, and six constraint/unresolved lines each. Do not conceal omitted files behind a claim that the brief captures the entire project.
