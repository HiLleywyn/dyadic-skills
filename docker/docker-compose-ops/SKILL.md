---
name: docker-compose-ops
description: Diagnose and operate existing Docker Compose projects, including service health, DNS, networks, mounts, environment configuration, targeted rebuilds, and container recreation. Use for Compose maintenance and service-to-service failures, while preserving project identity and persistent data.
---

# Docker Compose Operations

Confirm the Docker context and existing Compose project before changing services. Preserve the current project name, Compose file order, profiles, environment sources, volume identities, and externally managed networks.

## Identify the project

```powershell
docker context show
docker compose version
docker compose ls
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Status}}'
```

Read the repository's operating instructions and derive project/service identity from running Compose labels when necessary. Set `$project`, `$composeFile`, and `$service` from that evidence. For multiple files or explicit environment files, include the original arguments in their original order:

```powershell
$composeArgs = @('--project-name', $project, '--file', $composeFile)
docker compose @composeArgs config --quiet
docker compose @composeArgs config --services
docker compose @composeArgs ps --all
docker compose @composeArgs logs --since 10m --tail 100 $service
```

Read logs privately and redact credentials or user content before quoting them. Full `docker inspect`, resolved Compose output, and `config --environment` can expose secrets; use targeted fields instead. See [Compose configuration](https://docs.docker.com/reference/cli/docker/compose/config/).

## Trace connectivity from the caller

1. Identify the exact caller, hostname, container port, and protocol. Check the failure from that container with a tool already installed there.
2. Inspect both containers' network membership and aliases. On a shared Compose network, use the service name or configured alias and container port; published host ports serve a different path. Container-local `localhost` refers to that container.
3. Test DNS, then TCP, then the service's health route, then the actual application request. Keep authentication failures separate from name resolution or connection errors.

Use stable service names instead of container IPs. Cross-project communication requires an intentionally shared network. Make durable alias/membership fixes in the Compose configuration; disclose a temporary `docker network connect` repair as runtime drift. See [Compose networking](https://docs.docker.com/compose/how-tos/networking/).

Do not rotate provider credentials because an internal hostname fails. Avoid retrying AI, payment, or other chargeable requests until their completion state is known; a transport timeout does not prove no work occurred.

## Preserve state before recreation

Compare the intended configuration with the running service before stopping it:

- Identify mounted named volumes, bind mounts, writable container-layer data, network aliases, restart policy, and startup command.
- Check environment key presence and compare necessary values privately. `.env` interpolation and container `env_file` are different mechanisms; values from the invoking shell or `environment` can override other sources. Consult [environment precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/).
- If the running container has required settings absent from available configuration, recover the intended source without printing secrets. Do not recreate from an incomplete Compose file and silently lose runtime configuration.
- Quiesce writers and use the application's supported backup process when persistent data or a migration is involved. A copy of a live database volume alone may be inconsistent.

For an authorized change to one service, choose the applicable command after resolving those checks:

```powershell
# Rebuild an image from the existing local build context.
docker compose @composeArgs up --detach --no-deps --build $service

# Apply a configuration change without an unnecessary rebuild.
docker compose @composeArgs up --detach --no-deps $service
```

These are alternatives. Include dependencies when the change actually requires them. Confirm local help before using version-dependent flags such as `--wait`. `restart` does not apply changed container configuration. See [compose up](https://docs.docker.com/reference/cli/docker/compose/up/).

Do not use `down --volumes`, prune commands, broad forced recreation, or project renaming as incidental cleanup. Keep the prior image identity and a viable rollback path when changing a live service.

## Verify recovery

Inspect the resulting image identity, startup state, relevant health check, and bounded logs. Wait for the specific readiness condition with a deadline. Then repeat the original caller-to-service operation and a meaningful application check. A running container or a healthy upstream provider alone does not establish that the user flow works.

Report which service changed, whether it was rebuilt or recreated, how configuration and data were preserved, the observed application result, and any remaining limitation.
