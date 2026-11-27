---
name: dyadic-extension-authoring
description: Create or update Dyadic skill bundles and specialist presets, or document implemented plugins and MCP services without widening runtime authority.
---

# Dyadic Extension Authoring

Use this workflow for a requested Dyadic extension, not merely because a task mentions an agent.
Inspect the closest maintained package and its actual runtime owner first. Read [package design](references/package-design.md)
for the supported structure and [validation](references/validation.md) before delivery.

Choose a skill for procedural knowledge, a bounded subagent for an independent task context, a native plugin
for an implemented tool family, and MCP for a separate service interface. Do not invent a manifest kind or
add credentials, hooks, an execution framework or a new permission system to make the package appear usable.

Keep SKILL.md concise, with a discriminating description, essential procedure and links to conditional detail.
Copy all referenced resources into the individual bundle. A script is justified by repeatable deterministic
work; it is not executed on installation. For a reviewer preset, prefer exact read-only tools, strict_tools
and memory off. Reuse a useful preset before adding another.

Preserve IDs and bump the manifest version when its instructions/resources change. Explain account installation,
On/Off, selected skills, visible schemas and execution authority separately. Default catalog availability does
not mean every account should install or enable the item.

Use the GitHub repositories (`HiLleywyn/Dyadic` and the public catalog and Matrix repositories) for Dyadic source and
GitHub Issues for issue tracking. Work in an isolated checkout when other models are active;
do not alter their branches or run production deployment as a packaging test. Report concrete package changes,
checks, source revision, missing capabilities and remaining behavioral validation.
