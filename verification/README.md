# Verification Evidence

[Collection](../README.md) · [Maintenance](../MAINTENANCE.md)

- [Validation receipt](validation.json): the `docs` plus `store` merge inputs, Windows environment, actual commands and case totals for the combined 61-skill collection.
- [JUnit cases](catalog.xml): 66 passing cases from the merged collection's local run, including deterministic package builds.
- [Package checksums](package-checksums.json): reproducible individual build artifacts.
- [Actions preview](actions-preview.json): historical `store`-branch server validation of the unchanged pipeline template; not a hosted run or a validation of this merged revision.

Regenerate this evidence after package changes. Parser acceptance, account installation and model behavior are different verification steps. No provider calls or live account installation were performed.
