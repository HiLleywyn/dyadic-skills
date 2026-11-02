---
name: windows-diagnostics
description: Investigate Windows process, port, file-lock, service, scheduled-task, startup, crash, and event-log problems using scoped PowerShell queries and Sysinternals. Use for host diagnostics and evidence-backed repairs; Windows Sandbox, WSL, and application-specific workflows have their own procedures.
---

# Windows Diagnostics

Start from the failing operation, exact error, approximate time, and affected executable or resource. Gather evidence with the current permissions before attempting a repair. Select the diagnostic branch that explains the symptom instead of collecting a full host inventory.

## Establish context

Record Windows build, PowerShell edition/version, and whether the current process is elevated. A Windows Terminal tab, a remote session, and a background task can have different users, permissions, environment, and working directories.

```powershell
$PSVersionTable | Select-Object PSVersion, PSEdition
Get-CimInstance Win32_OperatingSystem |
    Select-Object Caption, Version, BuildNumber, LastBootUpTime
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
```

Treat access-denied and unavailable properties as limits of the observation. They do not prove a resource is absent. If a command needs elevation, identify that boundary and use an authorized elevated session; secure UAC interaction remains with the user.

## Ports and processes

For a reported TCP port conflict, set `$port` to that port and inspect its listener:

```powershell
Get-NetTCPConnection -LocalPort $port -State Listen |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

Use `Get-NetUDPEndpoint` for UDP. Inspect each returned owner with a distinct variable, avoiding PowerShell's read-only `$PID`:

```powershell
Get-Process -Id $ownerProcessId |
    Select-Object Id, ProcessName, StartTime, Path
```

Match the executable, start time, user, parent process, and service association before stopping anything; PIDs can be reused. Inspect command-line arguments only when needed and keep credentials out of quoted evidence. Prefer a targeted graceful application/service stop for an authorized repair. Do not kill every process sharing a name or alter global TCP settings to fix one listener.

## Events, services, and tasks

Bound event queries by time, relevant log/provider, and count. This example targets recent Application events; narrow it further after finding the provider:

```powershell
$startTime = (Get-Date).AddMinutes(-15)
Get-WinEvent -FilterHashtable @{LogName='Application'; StartTime=$startTime} -MaxEvents 50 |
    Select-Object TimeCreated, ProviderName, Id, LevelDisplayName, Message
```

Correlate event timestamps with the reproduction. A nearby warning is not proof of the cause. See [Get-WinEvent](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent).

For a service, query its exact name and inspect its startup mode, account, dependencies, executable, and recent failure. For a scheduled task, inspect its exact task path/name, principal, action, working directory, triggers, conditions, last run, and result. A task marked Ready does not prove its action succeeded. Reproduce under the actual task user and environment before changing permissions or triggers.

## File locks, hangs, and crashes

Use the smallest relevant [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/) tool, checking whether it is already installed before downloading anything:

| Evidence needed | Tool and method |
| --- | --- |
| Owner of an open file | [Handle](https://learn.microsoft.com/en-us/sysinternals/downloads/handle) or Process Explorer; search the exact path or a narrow distinctive fragment. Handle requires administrator rights. |
| File, Registry, or process activity during one failure | [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon); filter to the relevant process/path, capture a short reproduction, then stop capture. |
| Hang or crash state | [ProcDump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump); choose the appropriate trigger, target process, dump size, and local output directory. |

A missing-file or access-denied event can be an expected probe; identify the event that explains the failed operation. Do not close raw handles with Handle's `-c` as routine remediation. Save work and stop the owning application normally when that repair is authorized.

Keep captures and dumps in a task-specific directory. Dumps can contain credentials and user data; inspect locally and upload only when the request authorizes sharing them. Avoid installing persistent monitoring, a global crash debugger, or startup instrumentation for a single diagnosis unless required and authorized.

## Repair and verification

Change the smallest component supported by the evidence, preserving unrelated services, task settings, and security configuration. For filesystem changes, resolve absolute targets and use PowerShell `-LiteralPath` operations. Keep an appropriate rollback path for configuration edits.

Repeat the original failing operation and inspect the relevant new evidence. Report the demonstrated cause, changes, observed result, and any permission or reproduction limit. Distinguish a hypothesis from a confirmed cause and a completed command from a restored user workflow.
