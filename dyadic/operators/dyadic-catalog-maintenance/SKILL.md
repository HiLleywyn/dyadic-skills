---
name: dyadic-catalog-maintenance
description: Maintain the separate lley.cat skills, agents and plugins repositories, preserve Dyadic snapshot provenance, build reviewed import packages and report runtime compatibility gaps. Use for catalog publication and synchronization, not a Dyadic production deployment.
---

# Dyadic Catalog Maintenance

Keep three distinct collections: skills are reusable instructions/resources, agents are identities and delegation configurations, and default plugins are catalog switches for server-implemented tools. A plugin manifest is not executable provider code, and a catalog push is not a product deployment.

Read the destination README, `collection.json`, `catalog.json`, `provenance.json` and compatibility report. Confirm the remote UUID and current branch. Use [lley.cat Git](../../../lley-cat/lley-git/SKILL.md) for the custom gateway and [Actions](../../../lley-cat/lley-delivery/SKILL.md) when configuring or running its checks.

Treat source-backed snapshots and repository-authored additions separately. Refresh official definitions from an immutable Dyadic revision and record each source path and SHA-256; retain licenses/resources. Keep Iris under `agents/iris` and delegated specialists under `subagents`. New repository-only roles do not become official defaults through naming or copied metadata.

Native catalog agents use `agent.json` plus adjacent `instructions.md`. The current portable converter does not join that pair. Build the agent repository’s native package ZIP instead. Its explicit `import.json` tools are review suggestions, with memory off, strict tools and delegated usage enforced by Dyadic. Legacy default agents inherit capabilities that are intentionally narrower in portable exports; describe that adaptation. A primary Iris replacement is not an ordinary Store import.

Run `python tools/catalog.py index`, `check`, and the repository CI entrypoint. Build deterministic archives with `python tools/catalog.py build`. For a complete agent bundle, pass `--skills ../skills`; dependency hashes must match the reviewed lock. Security skill exports include their shared standards inside each archive. Never execute a downloaded skill script merely to install it.

Check ordinary and dependency-bundled exports using the target Dyadic revision’s existing inert package inspector when available. Record that revision and distinguish parser acceptance from a real account installation, runtime permissions, live providers and visible behavior. Keep executable plugin descriptors out of the instruction-import path.

Publish only the intended repositories. Verify remote HEAD and raw-file bytes against the commit, and retain validation/build evidence. Normal git.lley.cat folder URLs currently contain query parameters that Dyadic rejects; use built ZIP uploads until the product changes. Report that as an integration gap instead of modifying Dyadic during a repository-only task.
