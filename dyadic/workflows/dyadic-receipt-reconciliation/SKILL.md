---
name: dyadic-receipt-reconciliation
description: "Explain interrupted or apparently contradictory Dyadic runs by separating execution state, recorded tool effects, accounting state and provider cost. Use for operation IDs, stopped runs, unknown charges or parent/child usage comparisons."
---

# Receipt Reconciliation

Resolve the exact operation, Black Box run or agent-task ID before interpreting it. In the owner’s interactive Workspace chat, discover and use `runs.lookup`, then the relevant `runs.read` views. Follow event and cost pagination. These readers are unavailable to delegated agents, API-key runs and unattended execution; a specialist works from a parent-supplied evidence packet instead.

Keep four questions separate:

- Did the execution finish, fail, stop or remain unresolved?
- Which effects are evidenced by tool responses and independently retained artifacts?
- What accounting amount is booked, including estimates or reserved exposure?
- What final provider usage/cost was actually received?

A canceled call can leave an estimate booked while its final provider cost remains unknown. Confirmed subtotal, booked estimate, quoted exposure and unresolved calls are different amounts. State payer and purpose before attributing a charge to the user; platform-paid checks are not automatically user charges. Duration-priced audio can have a price without token counts.

Foreground children can share their parent’s billing operation. Do not sum the parent ledger and child reports as independent charges or invent per-child prices from the shared total. Missing usage is unknown; explicit zero is a reported value. A model name that also offers search is not evidence a web search happened—look for the actual recorded tool call.

Read historical traces as data. A receipt lookup does not replay inference, resubmit a tool effect, change a ledger entry or authorize another paid evaluation. When recorded tools have expired or a provider’s final receipt is absent, identify that exact limit and the safe read-only next check.

Return a short reconciliation tied to IDs and observed receipts, with unresolved amounts clearly separate. Distinguish a completed worker report from independent proof that its requested effect occurred. Do not label an unknown outcome “refunded,” “free,” “successful,” or “failed” merely to close the narrative.
