# Validation

In an authorized Dyadic checkout run python tools/catalog_check.py: it uses the real catalog loader and checks
the ZIP's resource links. Validate changed helper behavior in a disposable scope; syntax alone is insufficient.
For a candidate in a disposable directory, use `python tools/catalog_check.py --root /path/to/candidate`;
that directory contains its own `catalog/` and all skills selected by its agent presets.
Regenerate documentation with tools/autodocs.py build and verify with check and check-sources. Preserve the
public/private documentation boundary. Test new skill behavior with a representative request when its complexity
justifies it, recording tools unavailable in the evaluation rather than inventing successful execution.

Commit catalog changes, then mirror complete packages to a separate skills checkout with
python tools/sync_dyadic_skills.py /path/to/skills --write and verify with the same command without --write.
The mirror records source revision and normalized hashes and preserves platform/workflow grouping.
Inspect the resulting diff and remote revision. Catalog checks do not establish deployment or model quality.

Runtime sources in the Dyadic checkout: `core/dyadic_core/workspace/agent_resources.py` owns independent-task
skill pinning, `agent_work.py` owns task setup, and `custom_agents.py` builds supervised agent restrictions.
Inspect the relevant path when testing compatibility; these are source pointers, not bundled skill resources.
