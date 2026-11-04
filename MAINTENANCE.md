# Maintenance

[Collection](README.md) · [Skills](https://git.lley.cat/r/1a151e58-468a-45f1-a028-92c95690ad68?ref=store) · [Agents](https://git.lley.cat/r/dadd28be-7d91-432f-beb0-00d285e8f02b?ref=store) · [Plugins](https://git.lley.cat/r/ae86ea71-cb4d-4fc5-9ec1-803f8f303989?ref=store)

Run with Python 3.11+ and PyYAML. The checked-in Actions template uses an owner-prepared image with these dependencies and runs offline.

1. Preserve the collection layout and unique IDs. Update the package’s actual instructions/metadata, not only its README.
2. For official snapshots, copy the complete intended files from an immutable Dyadic revision, retaining attribution and resources. Update `provenance.json` from the source bytes. Its validator rejects undocumented drift.
3. Run `python tools/catalog.py index`, then `python tools/catalog.py check` and `python .lley/run.py`. Indexing refreshes navigation data; it does not bless snapshot hashes.
4. Run `python tools/catalog.py build`. Archives have sorted entries and fixed timestamps; `dist/checksums.json` records actual SHA-256 and size. No bundled script is executed by these steps.
5. For agents, preserve `agents/` versus `subagents/`. Review `import.json` permission suggestions and the linked skills in `compatibility/skill-dependencies.json`. A dependency update must refresh its reviewed content hash. Use `--skills ../skills` for a complete agent bundle.
6. Validate the exported bytes with the target Dyadic revision’s existing inert package inspector before claiming importer compatibility. Account installation, live tools, providers and visible delivery require separate evidence.
7. Push the intended commit, verify remote HEAD, and compare remote raw files at that commit. Keep the three catalogs cross-linked. Report product blockers in `COMPATIBILITY.md` instead of treating a repo update as a deployment.

The same `tools/catalog.py`, tests and CI runner are copied across the three repos so each clone validates offline on its own. When changing that shared tooling, update all three and run their checks. The source inventories and provenance files differ by collection.

## Actions

`.lley/pipeline.json` is a custom lley.cat Actions template, not a GitHub workflow. It runs collection tests and builds archives, publishes JUnit results and the collection/checksum artifacts, and has no deployment or credentials. Saving a template does not activate a repository. Inspect the server’s current configuration/version and activation before running it. An owner must activate new repositories; a PAT cannot bypass that gate. See the compatibility report for this delivery’s actual hosted-run status.
