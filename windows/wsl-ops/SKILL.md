---
name: wsl-ops
description: Diagnose and manage Windows Subsystem for Linux distributions, Windows/Linux paths, shell environments, networking, interoperability, configuration, and backups. Use for WSL-specific failures and requested distro maintenance; application bugs inside an otherwise healthy Linux environment do not require this skill.
---

# WSL Operations

Identify the exact Windows host, distribution, Linux user, and affected process before changing anything. A distribution may host editors, containers, remote sessions, and unrelated jobs. Preserve those sessions while diagnosing the requested problem.

## Locate the failing environment

From Windows, inspect without changing the default distro:

```powershell
wsl.exe --status
wsl.exe --version
wsl.exe --list --verbose
```

Use the installed `wsl.exe --help` when an option is unavailable. Select `$distro` from the actual list and `$linuxUser` from the task; do not assume Ubuntu, the default distro, or root. Commands using `--exec` start a stopped distro, so target only the environment relevant to the request:

```powershell
wsl.exe --distribution $distro --user $linuxUser --exec id
wsl.exe --distribution $distro --user $linuxUser --exec uname -r
wsl.exe --distribution $distro --user $linuxUser --exec ps -eo pid,ppid,comm
```

See Microsoft's [command reference](https://learn.microsoft.com/en-us/windows/wsl/basic-commands). Record which side ran each command and distinguish a WSL platform failure from a failing Linux application.

## Paths, shells, and interoperability

- Use Windows paths for Windows tools and Linux paths for Linux tools. Convert with `wslpath` inside the selected distro when needed. Do not translate paths by blindly replacing slashes: mounts can be customized.
- Reproduce shell problems in the actual launching shell or wrapper. A fresh login shell can have different environment variables, startup files, working directory, and executable resolution.
- Check the relevant executable with `command -v` or `type -a` inside that shell. Inspect only the necessary variable names and whether their values are set; avoid dumping the entire environment or printing credentials and private endpoint values.
- For Windows executable failures inside WSL, inspect interoperability settings and the active `/proc/sys/fs/binfmt_misc/WSLInterop` entry if present. Do not register a handler or overwrite boot configuration until evidence identifies it as the fault.
- Identify whether a command starts a Windows process, a distro process, or a container process before inspecting or terminating it. Match the executable, user, parent process, and session instead of matching a product name alone.

## Network failures

Test the failing connection from its originating environment. Separate DNS resolution, routing, TCP reachability, TLS, HTTP status, and application authentication. A host browser succeeding does not prove the same path works inside WSL or a container.

Determine NAT versus mirrored networking before choosing an address. Under NAT, Linux-to-Windows access generally needs the Windows host address; mirrored networking supports localhost between them. Check listener bindings, relevant VPN/proxy settings, and specific firewall rules before editing configuration. Avoid hardcoding a transient WSL IP, replacing `resolv.conf`, or disabling a firewall as a first repair. See [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking).

## Configuration and recovery

`%UserProfile%\.wslconfig` affects the WSL 2 VM globally; `/etc/wsl.conf` configures an individual distro. Preserve unrelated sections and confirm build support for a proposed option using the [configuration reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

Read running processes and explain the affected scope before a disruptive restart. For an authorized restart of one distro, use:

```powershell
wsl.exe --terminate $distro
```

Use `wsl.exe --shutdown` only when the requested repair requires stopping all running distributions and that wider interruption is authorized. Check for Docker Desktop and active remote sessions first. After a restart, verify both the changed setting and the original failing operation; process startup alone is insufficient.

For requested backup or migration, export to a new path and check the native exit code and resulting file. An export is not application-consistent by itself; quiesce databases and writers when consistency matters. Import a restore under a distinct name and location, then inspect its user, files, and application behavior before treating it as verified. Never use `--unregister` as routine repair: it deletes the distro's data.

Report the selected distro/user, relevant evidence, changes, impact on sessions, and the observed result. Keep backups and unrelated distributions intact.
