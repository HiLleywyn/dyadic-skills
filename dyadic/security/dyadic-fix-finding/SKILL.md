---
name: dyadic-fix-finding
description: Implement a narrow, authorized source change for a validated security vulnerability and add focused regression coverage while preserving intended behavior. Use only when the user explicitly asks to fix a specific finding; do not use for speculative hardening, ordinary bug cleanup, deployment, or unrelated refactoring.
---

# Dyadic Fix Finding

Remediate the validated root cause with the smallest maintainable change and leave a verifiable evidence trail. A security fix is not complete merely because the exploit test stops passing; intended behavior and adjacent representations must remain correct.

Read [safe testing](../_shared/safe-testing.md), [evidence and provenance](../_shared/evidence-standard.md), and the validated finding. Use `$dyadic-verify-fix` after implementation when the user asks for independent verification.

## Preconditions

Require:

- a validated finding ID and immutable vulnerable revision;
- explicit authorization to modify the named repository or patch artifact;
- current working-tree status and ownership of existing changes;
- documented intended behavior and compatibility requirements;
- a focused proof or regression condition;
- repository instructions, test conventions, and release/backport expectations.

Do not discard, reset, overwrite, or reformat unrelated user work. If the target lines overlap unexplained local changes, inspect provenance and stop for direction when the changes cannot be preserved.

## Design the remediation

State the security invariant to enforce. Evaluate fixes at the earliest stable boundary that sees the final representation and correct identity. Prefer structural prevention over scattered filtering:

- authorize the actual object at the point of use;
- reject redirects or revalidate the final destination when policy requires it;
- return generic external errors and keep redacted diagnostics internal;
- bind actor and tenant context into queued work;
- enforce parser and sink on the same canonical form;
- consume nonces and commit state atomically with the protected action;
- add per-request and aggregate size/time/output/concurrency/cost budgets;
- remove dangerous capability rather than block a few payload strings;
- use parameterized APIs and contextual output encoding.

Account for alternate routes, serializers, versions, fallbacks, caches, retries, and error paths. Do not fix only the supplied PoC string.

## Implement surgically

Modify only files required for the root-cause fix and regression. Preserve public interfaces unless the security requirement demands a documented breaking change. Follow repository style and existing helpers. Avoid opportunistic dependency updates, renames, formatting sweeps, dead-code cleanup, or architecture rewrites.

Never embed real credentials or victim data in a test. Use deterministic synthetic fixtures. For sensitive logs and responses, assert absence as well as expected generic behavior.

## Regression coverage

Tests should include:

1. the original exploit or semantic condition;
2. a negative control showing the assertion would detect the old behavior;
3. expected legitimate behavior;
4. applicable variants across alternate representations or routes;
5. debug/development and production behavior when they differ;
6. failure, retry, transaction, and cleanup behavior when relevant.

Prefer a focused test near existing coverage. If the repository cannot run locally, provide a proposed test and state it was not executed.

## Verify locally

Run the smallest relevant test first, then the component suite, static/lint/type checks, and broader tests proportional to risk. Record exact commands and outcomes. Re-run the original proof against the patched artifact. Inspect the final diff for secret leakage, debug code, weakened tests, unrelated changes, and generated artifacts.

## Deliverable and mutation boundary

Provide:

- finding fixed and invariant enforced;
- files changed and why;
- regression tests;
- commands and results;
- compatibility or migration notes;
- remaining defense-in-depth ideas separated from required remediation;
- unverified environments;
- final diff summary.

Do not commit, push, open a pull request, merge, deploy, rotate credentials, notify users, or publish an advisory unless the user separately requests that action. A patch can be complete without being deployed; report those states separately.
