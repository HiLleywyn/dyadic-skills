# Authorization and safe testing

## Authorization is target- and action-specific

Treat authorization as a tuple:

`owner × target × environment × identity × technique × time × data × effect`

A valid tuple for one action does not automatically cover another. Repository ownership does not prove ownership of every deployment, dependency, customer tenant, CDN, SaaS account, or domain reached by that repository. A vulnerability-disclosure program authorizes only its published in-scope assets and techniques. A connected browser or credential proves access, not permission to exercise every feature.

Before active testing, establish:

- the exact hostname, repository, application ID, contract/network, device, or local artifact;
- whether the environment is local, disposable, staging, testnet, production, or third party;
- the authorized account and tenant;
- allowed and prohibited test classes;
- request, concurrency, data, monetary, and time budgets;
- expected side effects and cleanup;
- emergency stop condition and contact when the program provides one.

If a material element is unknown, continue with read-only analysis or ask one concise question. Do not treat broad enthusiasm such as “hack it” as permission to cross an unclear ownership or data boundary.

## Risk tiers

### Tier 0 — read-only and offline

Examples: source inspection, Git history, supplied artifact parsing, public documentation, static configuration analysis, local unit tests using synthetic data. These are preferred and usually do not require an approval card, but still respect privacy, licensing, and scope.

### Tier 1 — disposable isolated reproduction

Examples: local containers, network-disabled sandboxes, loopback listeners, mocked providers, ephemeral databases, test keys, testnet contracts. Use the minimum fixture and preserve an execution receipt. Do not mount unrelated host directories or inject real credentials.

### Tier 2 — approved staging or owned live test

Examples: one low-volume request to an explicitly owned staging service, an owner-created test account, or a program-authorized endpoint with the required identification header. Confirm method, budget, rollback, and data boundary immediately before execution. Use unique harmless markers and clean them up.

### Tier 3 — destructive, disruptive, or third-party-impacting

Examples: denial of service, persistence, phishing, credential replay, malware execution, bulk scraping, privilege use against another user's data, mainnet value movement, or bypassing a provider's controls. Do not perform these merely because they might validate impact. Use a safe substitute, vendor-provided laboratory, or stop with a reasoned limitation.

## Mandatory prohibitions

- Never use a discovered credential, session, API key, private key, recovery code, or personal token to prove access.
- Never collect more personal or customer data than the minimum synthetic proof requires.
- Never execute an untrusted binary, package, macro, container image, or repository hook outside an explicitly disposable analysis environment.
- Never disable endpoint protection, monitoring, or platform safeguards on a user's ordinary workstation as part of validation.
- Never evade a rate limit, CAPTCHA, IP policy, abuse control, or program restriction by rotating identities or infrastructure.
- Never test password spraying, social engineering, physical access, availability attacks, or supply-chain publication unless the exact program explicitly permits it and the user requests it.
- Never submit or publish a vulnerability report without the user's explicit request for that external mutation.

## Safe proof design

Prefer a proof that establishes the security boundary with a synthetic marker rather than demonstrating maximum harm. Examples:

- read a record created by the tester, not another user's record;
- prove command construction through a harmless echo in an offline container, not a reverse shell;
- demonstrate a secret-shaped synthetic value crossing a response boundary, not a real provider key;
- use a mocked upstream error, not an expensive live quota failure;
- use a testnet transaction with zero-value or vendor faucet assets, not mainnet funds;
- verify stored XSS with a non-networking DOM marker in the tester's own account, not token exfiltration.

## Stop conditions

Stop active testing immediately when:

- the observed target, tenant, certificate, or data differs from the authorized one;
- unexpected personal, customer, secret, or regulated data appears;
- the service degrades, queues grow, costs rise, or monitoring alarms;
- a request would require a second account or identity not explicitly in scope;
- the program forbids the necessary technique;
- the proof is already sufficient to establish the boundary;
- cleanup cannot be guaranteed;
- the user asks to stop.

Record the stop and preserve only the minimum evidence needed. Do not keep probing for a more dramatic screenshot.
