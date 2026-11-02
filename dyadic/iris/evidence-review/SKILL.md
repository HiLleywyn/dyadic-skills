---
name: "evidence-review"
description: "Check tool outcomes, persisted artifacts and provider usage without trusting completion claims."
---

# Execution Evidence Review

Distinguish a model report, a tool response, an independently observed effect and a provider usage receipt.
For agent work, open Agent Tasks > Compare Results. Reported Completion only means the worker produced an answer.
Artifact Checks read persisted output bytes and show hashes; a contains check proves only that exact byte substring.
Recorded Tools may be incomplete after retention; report omitted rows. A successful tool response is not proof of every
claimed effect. Preserve operation IDs, read-back receipts, exact commands and test outputs when present.
Input/output/cache counts come from recorded provider usage. Missing is unknown; zero cached tokens is a real count
only when the provider explicitly reported zero. Estimated tariffs and token-priced estimates are not provider cost
receipts. Foreground children share a parent billing operation and cannot be individually priced from that ledger.
Compare models only on the same inputs, instructions, checks and relevant constraints. Do not route automatically
based on one confident answer, a cheap estimate or an incomplete receipt. No live provider evaluation is authorized
by this skill alone. The owner starts and pays for each bounded workload through the existing task controls.
