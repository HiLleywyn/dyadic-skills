# Package Design

Official source: catalog/skills/<id>/{skill.json,SKILL.md,references/,scripts/},
catalog/agents/<id>/{agent.json,instructions.md}, catalog/plugins/<id>/plugin.json.
Portable imports use dyadic-package.json and reviewed referenced files; use examples/agent-package in the
Dyadic checkout as the current example. The native loader, not a foreign framework manifest, is authoritative.

Skill frontmatter has name and description. The folder, name and manifest id match. Every local Markdown link
must resolve inside the installed bundle. No ../_shared dependencies. Store semantic versions differ from
the account store's integer versions. At most 500 files, 25 MB unpacked and 50 MB uploaded are accepted.

Tool requirements describe compatibility, not grants. Discover tools with tools.load; read installed resources
with skills.read(name=...,path=...). Agent tools stay bounded by parent and account restrictions. Supervised
children are one generation deep and share finite budgets. Owner-started independent tasks only carry selected
pinned SKILL.md text, not referenced resources or executable helpers; say when a package requires those inputs.

The official Documentation MCP is implemented separately from the three catalog kinds. External Black Box and
Lley services require their own current authentication and scopes. Do not make them implicit default connections.
