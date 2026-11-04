---
name: dyadic-api-integration
description: Integrate an application with Dyadic APIs, SDKs or MCP using the correct host, credentials, contract and execution lifecycle.
---

# Dyadic API Integration

Read [API surfaces](references/api-surfaces.md) when choosing a client or diagnosing a route. Discover the
official Dyadic Documentation MCP if available; use its `api` tool for exact methods, paths and schemas.
Otherwise read the supplied source contract or public developer reference. A source snapshot may differ from
the running service, so retain the contract version and source hash when available.

Start with the requested workflow and the caller's principal: API key, owner session or administrator session.
Do not invent public SDK methods for Workspace-only controls. Enable no account capability merely to make an
example run. Use only the tools available in this context; the skill is not an HTTP client or credential store.

Keep keys in the application's server or an existing configured connection. Match the base URL to the SDK's
convention. Choose a cheap authorized read to verify configuration before inference or mutation. For writes,
prepare the concrete request and use the real execution approval flow under the user's existing task scope.

Use [lifecycle and evidence](references/lifecycle.md) for streaming, retry and cancellation. Check returned
IDs, terminal status, persisted effects and delivery separately. Document compatibility limits and failed or
unexecuted checks. A useful handoff includes the chosen contract, a minimal runnable example with environment
variable names, required capability switches and the actual validation performed.
