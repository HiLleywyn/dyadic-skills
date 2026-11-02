---
name: winget-setup
description: Use WinGet to discover exact Windows packages, install or update requested tools, manage package pins, export/import tool setups, and bootstrap WinGet inside Windows Sandbox. Use for Windows package management and reproducible developer environments, with explicit package identity and scope.
---

# WinGet Setup

Install or change only the packages required by the user's request. Distinguish preparing a package list from executing it, and distinguish the Windows host from a Windows Sandbox guest before every installation.

## Inspect availability and select a package

```powershell
Get-Command winget.exe -ErrorAction SilentlyContinue
winget --version
winget --info
winget source list
```

If WinGet is missing, check App Installer availability and the current user registration; do not copy another user's executable or silently switch to an unofficial package manager. See Microsoft's [WinGet overview](https://learn.microsoft.com/en-us/windows/package-manager/winget/). Use local subcommand help for version-dependent flags.

Choose `$packageId` and `$source` from actual search results and the requested publisher. Check existing installation, publisher, version, architecture, installer type, and supported user/machine scope:

```powershell
winget search --query $query --source $source
winget show --id $packageId --exact --source $source
winget list --id $packageId --exact
```

Use exact IDs and an explicit source to avoid ambiguous display-name matches. Prefer the installed tool and compatible version when they already satisfy the task. Do not replace a working toolchain simply because another version is available.

## Install or update the requested tool

For an authorized installation after inspecting package details:

```powershell
winget install --id $packageId --exact --source $source --scope user
```

Use `--scope user` only if that package supports it and it fits the request. Choose machine scope when required and authorized. Add `--version` for an available requested version and `--architecture` when the architecture matters. Do not silently fall back from an unavailable version or scope. See [install options](https://learn.microsoft.com/en-us/windows/package-manager/winget/install).

Target updates with `winget upgrade --id $packageId --exact --source $source`; inspect current and proposed versions first. Avoid `upgrade --all`, `--force`, uninstall/reinstall, or pin removal as incidental repair.

Use agreement acceptance and silent/noninteractive flags only in a workflow authorized to accept those agreements and install unattended. Do not bypass installer hash checks or Windows policy to make an installation succeed.

Check the native exit code immediately and retain the relevant diagnostic log on failure. If elevation or an interactive installer prevents completion, report that state instead of treating a launched installer as a successful install. After success, verify the installed package and its actual executable/version. PATH changes may need a fresh process; do not rewrite the global PATH to compensate for one stale shell.

## Reproduce an environment

For an authorized inventory export, choose a task-specific `$exportPath`:

```powershell
winget export --output $exportPath --include-versions
```

Review the JSON before sharing or using it. An export can include unrelated installed applications; keep only the intended tool set in a prepared setup list and record packages WinGet could not match. Versioned exports do not guarantee an older installer remains available. See [export](https://learn.microsoft.com/en-us/windows/package-manager/winget/export).

Import is an installation operation, so inspect package IDs, sources, and versions before an authorized run:

```powershell
winget import --import-file $exportPath --no-upgrade
```

Use `--no-upgrade` when existing installations should remain at their current versions. Do not add `--ignore-versions` or `--ignore-unavailable` to hide a mismatch; report what could not be reproduced. Verify each required tool after [import](https://learn.microsoft.com/en-us/windows/package-manager/winget/import).

For requested [pins](https://learn.microsoft.com/en-us/windows/package-manager/winget/pinning), inspect `winget pin list` and choose normal, blocking, or version-gating behavior deliberately. Pins govern WinGet updates; they do not prevent an application's own updater from changing its version. Preserve unrelated pins.

## Windows Sandbox bootstrap

Sandbox lacks WinGet and Microsoft Store by default. Only when an online guest setup is requested, run Microsoft's documented bootstrap inside that guest:

```powershell
Install-PackageProvider -Name NuGet -Force | Out-Null
Install-Module -Name Microsoft.WinGet.Client -Repository PSGallery -Force | Out-Null
Repair-WinGetPackageManager -AllUsers
```

Confirm the guest identity and networking before running it, and verify `winget --info` afterward. The guest installation disappears when Sandbox closes. For offline tests, prepare verified installers as inputs instead of enabling guest networking without regard to the task.

Report installed/updated/skipped/failed packages, observed versions, scope, any reboot or fresh-shell requirement, and the location of the setup list or logs.
