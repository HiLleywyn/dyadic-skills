---
name: dyadic-verify-fix
description: Verify that a proposed patch or release remediates a specific validated vulnerability without breaking intended behavior or leaving equivalent bypasses. Use when the user asks to verify a security fix; do not automatically modify the patch, declare unrelated findings, or treat test success as proof of deployment.
---

# Dyadic Verify Fix

Independently determine whether the candidate fix closes the original attack path at the assessed revision and whether the surrounding security invariant now holds.

Read [validation rubric](references/validation-rubric.md), [evidence and provenance](references/evidence-standard.md), [safe testing](references/safe-testing.md), and the original finding plus its proof.

## Freeze the artifacts

Record:

- original vulnerable revision and finding ID;
- patch, pull request, commit, or proposed fixed release revision;
- base/head relationship and diff digest;
- dirty state and uncommitted changes;
- test environment and dependency versions;
- claimed fix and claimed affected/fixed versions.

Verification is revision-specific. Do not combine a source patch from one commit with a deployed binary from another. If runtime identity cannot be established, verify source and state that deployment remains unverified.

## Restate the invariant and exploit

Describe the original source, failed control, sink, impact, prerequisites, and the invariant the fix must enforce. Re-run or reconstruct the original proof against the vulnerable revision when safe and practical so the test is known to detect the defect. If that baseline cannot be executed, preserve the original validated receipt and explain the limitation.

## Review the patch structurally

Determine whether the change addresses the root cause or only the supplied payload. Inspect:

- all callers, alternate routes, serializers, protocol versions, redirects, fallbacks, and error paths;
- canonicalization order and final representation;
- actor, tenant, origin, scope, and approval binding;
- transaction, retry, cache, queue, and concurrency behavior;
- limits at request and aggregate levels;
- debug, development, and production modes;
- migrations, defaults, feature flags, and backward compatibility;
- tests that were changed or removed.

Look for regressions introduced by the fix: fail-open behavior, new denial of service, information leakage, double encoding, authorization bypass, race, broken cleanup, or incompatible state.

## Execute verification matrix

At minimum:

1. **exploit regression**  -  original proof no longer achieves unauthorized effect;
2. **negative control**  -  test would still fail against vulnerable behavior or an intentionally vulnerable fixture;
3. **legitimate behavior**  -  supported use case still works;
4. **variant coverage**  -  equivalent encodings, routes, redirects, representations, or identities are handled;
5. **failure behavior**  -  errors remain safe and do not partially commit;
6. **component regression**  -  relevant existing suite passes;
7. **build/static checks**  -  applicable lint, type, analyzer, or compilation succeeds.

Use synthetic data and isolated environments. A test named after the vulnerability is not evidence unless its assertions exercise the boundary. Preserve commands, output, cleanup, and skipped variants.

## Decide

Return one verdict:

- **verified fixed**  -  root cause and supported variants are closed; regression and legitimate behavior pass;
- **partially fixed**  -  original proof is blocked but equivalent paths or supported conditions remain;
- **not fixed**  -  original unauthorized effect remains;
- **regressed**  -  security issue is closed but the patch introduces a material new defect;
- **inconclusive**  -  missing build/runtime/deployment evidence prevents a decision.

Assign confidence and list exact tested revisions. If a release or deployment is claimed, separately verify artifact/runtime identity or mark it outstanding. Do not edit the patch during verification; return actionable evidence to `$dyadic-fix-finding` if changes are needed.

## Output

Provide verdict, invariant, diff review, test matrix, commands/results, variant analysis, compatibility observations, untested conditions, and release/deployment boundary. Update the finding record only when the user asks to persist status. Do not merge, deploy, close an external report, or announce remediation without separate authorization.

## Installed Resources

Use `tools.load(inventory=true)` to discover enabled skills and permitted tools. Load the skills group,
then read this package with `skills.read(name="dyadic-verify-fix", path="SKILL.md")`.
Read linked references using the same skill name and their bundle-relative paths. Cross-skill `$name`
references describe optional workflows, not callable tool names; discover an enabled sibling first.
If it is unavailable, perform the supported part directly and record the remaining phase as unexecuted.

For a durable record, use the [finding schema](references/finding.schema.json). The bundled
[validator](scripts/validate_finding.py) checks record invariants without third-party packages; it does
not establish that a finding is true. Run it only through an authorized execution tool.
