---
name: release-verification
description: Verify that a specified software revision or release artifact reached the intended environment and that the affected user workflow works. Use after deployments, beta distribution, or release requests, including checks of runtime identity, artifact provenance, readiness, API behavior, and visible UI delivery. Verification alone does not authorize deployment or publication.
---

# Release Verification

Establish a chain of evidence from the intended source revision to the built artifact, running environment, and user-visible result. Adapt the checks to the affected feature and the project's release procedure. Keep the work scoped to the requested environment and revision.

## Establish the target

Record the repository, full source commit, relevant local changes, release version/build, artifact or image identity, target environment, and affected user flow. Read the repository's release instructions and use its actual delivery provider; do not assume GitHub Actions, a particular container platform, or a mobile distribution service.

Verification, building, deployment, release publication, rollout activation, and notifying people are different actions. Perform the actions already authorized by the user's request and identify any actual missing authorization before an additional mutation. Do not activate disabled delivery pipelines to gather evidence.

## Match source, artifact, and runtime

- Confirm the checkout's commit and working-tree state. A build from local changes does not exactly represent the committed revision unless those changes are accounted for.
- Record the build's source metadata, immutable image digest or artifact checksum, and native version/build number when applicable. A mutable tag or friendly version string alone cannot establish provenance.
- Read revision/build metadata from the running application or deployment. Check independently deployed components separately, such as API, web frontend, workers, and mobile packages.
- If the runtime lacks revision metadata, triangulate from build records, artifact identity, running image identity, and feature behavior. State the remaining uncertainty; do not claim an exact runtime revision from the checkout alone.
- For a distributed download, compare the downloaded artifact with the built/published checksum when access and download are part of the request. Distribution acceptance does not establish installation or execution on a device.

Capture timestamps with an explicit timezone when sequencing a deployment and its observations. Keep secrets, access tokens, signed download URLs, and user data out of evidence intended for sharing.

## Check readiness and the affected behavior

Wait for the actual readiness signal with a deadline appropriate to the deployment. Check health state, startup errors, and relevant dependencies. A launcher exiting, an upload being accepted, or a container entering Running is an intermediate observation.

Choose the smallest meaningful check for each changed behavior. Use repository-required gates, then focus additional testing on concrete risks or failures. Repair a broken test harness before relying on its results, and distinguish a harness failure from a product failure.

For an API path, verify the relevant authentication, expected payload/state change, and error behavior. Use the approved test account and environment. Avoid chargeable retries or duplicate external side effects when completion is uncertain; inspect the original request or stored state first.

For a visual change, inspect the actual rendered UI at the relevant desktop/mobile viewport or device class. Exercise the interaction and look for layout overlap, inaccessible controls, stale assets, and visible state updates. A screenshot at one size does not establish every breakpoint or physical-device behavior.

For generated media or asynchronous delivery, follow the result through generation, storage/metadata, API/event delivery, and rendering in the consuming interface. A stored image or success event is intermediate evidence; verify that the intended user can actually see or use the result.

For billing or usage displays, compare the displayed values with the relevant settled provider/ledger records. Keep elapsed duration, billable duration, cost, and unavailable token counts separate. Do not convert missing data into a fabricated zero or an unlabelled estimate.

## Record the result honestly

Keep a compact evidence table when several components or checks are involved:

| Check | Expected | Observed evidence | Result or limit |
| --- | --- | --- | --- |
| Source/artifact/runtime identity | Intended revision and build | Commit, digest, or runtime metadata | Verified or remaining uncertainty |
| Readiness | Relevant service is ready | Health result and bounded logs | Passed, failed, or pending |
| Affected user flow | Requested behavior occurs | API result, UI observation, or device evidence | Passed, failed, or not tested |

If a deployment is still settling, recheck readiness within the deadline. Investigate a specific failure before retrying. Do not roll back, republish, or repeatedly redeploy unless the task's authorization and release procedure cover that action.

Report the verified revision/artifact, environment, observed user outcome, and material limits. Separate local tests, remote deployment, visible UI validation, and physical-device checks. Mark skipped or unavailable checks explicitly. Do not describe a partial delivery as shipped and verified when a required step remains unresolved.
