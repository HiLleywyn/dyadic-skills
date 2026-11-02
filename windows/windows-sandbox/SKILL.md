---
name: windows-sandbox
description: Set up, configure, launch, automate, and troubleshoot Microsoft Windows Sandbox on Windows. Use for .wsb configuration files, disposable Windows app or installer tests, mapped folders, logon scripts, and the wsb CLI. Does not govern Codex execution sandbox permissions.
---

# Windows Sandbox

Use Microsoft's disposable Windows desktop for the requested task. Creating a configuration or explaining Sandbox does not authorize enabling Windows features, changing host security settings, or running the supplied application.

## Choose the workflow

- For a configuration request, create a `.wsb` file and any required guest script, then validate them without launching unless launch was requested or is part of the authorized test.
- For an application test, stage the necessary inputs, choose the required network access and output location, run the test inside the guest, and collect evidence before closing it.
- For command automation, detect the installed `wsb.exe` and read [references/cli.md](references/cli.md). Use local command help to confirm capabilities.
- For setup or failures, inspect the host first and change only the component relevant to the observed problem.

Sandbox does not inherit host-installed applications. Closing it discards guest state; Windows 11 22H2 and later can retain state across restarts initiated inside the guest. Export required results before closing. Microsoft currently documents one running instance at a time; preserve an existing session instead of stopping it to make room. Supported editions include Pro, Enterprise, and Education; Home is unsupported. See the [overview](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/).

## Inspect and enable when requested

Read the host edition, build, virtualization indicators, and available launchers:

```powershell
Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' |
    Select-Object EditionID, DisplayVersion, CurrentBuildNumber, UBR
Get-CimInstance Win32_ComputerSystem | Select-Object HypervisorPresent
Get-CimInstance Win32_Processor |
    Select-Object Name, VirtualizationFirmwareEnabled, SecondLevelAddressTranslationExtensions
Get-Command WindowsSandbox.exe, wsb.exe -ErrorAction SilentlyContinue |
    Select-Object Name, Source
```

Treat these as diagnostic indicators, especially when Windows itself is a VM. Check the [installation requirements](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-install): supported Windows version and edition, AMD64 or supported Arm64, firmware virtualization, at least 4 GB RAM, 1 GB free disk, and two CPU cores. A VM needs nested virtualization enabled by its host. Do not change firmware or upgrade a VM configuration as incidental troubleshooting.

The following feature query and enable command require an elevated PowerShell session. Query first; enable only for an authorized setup task when the feature is disabled:

```powershell
Get-WindowsOptionalFeature -Online -FeatureName 'Containers-DisposableClientVM'
Enable-WindowsOptionalFeature -Online -FeatureName 'Containers-DisposableClientVM' -All -NoRestart
```

Report any `RestartNeeded` result. Restart the host only when authorized. If elevation is unavailable, report that limitation and provide the command for an administrator. A denied feature query does not prove the feature is disabled.

## Create the configuration

For unknown files, start with offline networking, disabled redirection, and a dedicated input folder mapped read-only. Enable capabilities needed by the user's task explicitly. Online development or installer tests may need networking; do not silently substitute an offline test for them.

Adapt this example from Microsoft's [sample configurations](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-sample-configuration). Replace `C:\SandboxJobs\Example\Input` with the actual staging directory and create that directory before launch. Stage only the files needed for this job, rather than sharing an entire profile or Downloads folder.

```xml
<Configuration>
  <VGpu>Disable</VGpu>
  <Networking>Disable</Networking>
  <AudioInput>Disable</AudioInput>
  <VideoInput>Disable</VideoInput>
  <PrinterRedirection>Disable</PrinterRedirection>
  <ClipboardRedirection>Disable</ClipboardRedirection>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\SandboxJobs\Example\Input</HostFolder>
      <SandboxFolder>C:\Input</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>explorer.exe C:\Input</Command>
  </LogonCommand>
</Configuration>
```

Consult the [configuration reference](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) when adding options:

- Boolean-like capabilities use `Enable`, `Disable`, or `Default`; `ReadOnly` uses `true` or `false`. Spell these explicitly, avoiding `Enabled` or `Disabled`.
- Host folders must exist. Use absolute paths. `ReadOnly` defaults to `false`, so always specify it.
- Writable mappings persist changes on the host after Sandbox closes. Add one dedicated output directory only when results must be exported; never grant write access to the original project just to collect logs.
- Networking, clipboard sharing, and audio input are enabled by default. Specify the intended behavior instead of depending on defaults.
- `ProtectedClient` can be enabled for additional isolation but can restrict file transfer. `MemoryInMB` sets guest memory; values below the minimum are raised to 2048 MB.

Generate XML with an XML writer or escape inserted text, particularly `&`, `<`, and `>`. Quoting for XML and quoting for the guest command are separate requirements.

## Run scripts and collect results

Keep multi-step work in a guest script mapped with the inputs. Reference its guest path in `LogonCommand`, for example:

```xml
<LogonCommand>
  <Command>powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Input\Run-Test.ps1"</Command>
</LogonCommand>
```

This example uses a process-scoped execution policy override in the guest; it does not change the host policy. Prefer Windows PowerShell (`powershell.exe`) unless the job installs PowerShell 7. Do not assume `pwsh`, Python, Git, a browser automation package, or other host tools are present.

If a program must modify its inputs, copy them from `C:\Input` into a guest working directory first. Run installers and application commands there. Record meaningful checks, native process exit codes, and exceptions. For unattended results, write a final completion record only after logs have been flushed, including success or failure and the relevant exit code.

When export is required, map an otherwise empty job output folder to `C:\Output` with `ReadOnly` set to `false`. Treat exported files as untrusted: inspect logs as data and do not automatically execute exported programs or scripts on the host. Do not place host credentials in staging folders or generated configs.

## Validate and launch

Check the actual file extension, XML syntax, every host directory, guest paths, and command quoting. XML parsing checks syntax only; it does not verify that Sandbox accepts a setting:

```powershell
$configPath = (Resolve-Path -LiteralPath '.\Job.wsb').Path
[xml]$config = Get-Content -LiteralPath $configPath -Raw
if ($config.DocumentElement.Name -ne 'Configuration') {
    throw 'Expected a Configuration root element.'
}
foreach ($mapping in $config.SelectNodes('/Configuration/MappedFolders/MappedFolder')) {
    if (-not (Test-Path -LiteralPath $mapping.HostFolder -PathType Container)) {
        throw "Missing host folder: $($mapping.HostFolder)"
    }
}
```

For an authorized interactive launch, open the resolved configuration through its `.wsb` association:

```powershell
Start-Process -FilePath $configPath
```

A successful launcher process is not evidence that the guest or test succeeded. Verify the guest desktop or a job-specific completion record. Use a bounded wait appropriate to the task; inspect the actual failure before retrying. Preserve outputs and any existing user session when finishing.

## Troubleshoot from evidence

Capture the exact error, Windows build, launch method, feature state if available, and the relevant configuration. Use Microsoft's [troubleshooting guide](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-troubleshoot):

| Symptom | Next check |
| --- | --- |
| Missing config or `ERROR_FILE_NOT_FOUND` | Resolve the actual `.wsb` path and check for a hidden `.txt` extension. |
| `E_INVALIDARG` | Inspect XML, setting values, mappings, and command quoting. |
| `REGDB_E_IIDNOTREG` or no hypervisor | Verify the optional feature, required reboot, firmware virtualization, and nested virtualization if applicable. |
| Settings enforced by administrator | Inspect applicable Sandbox policy; report the restriction. |
| Store upgrade or endpoint failure | Check host Internet, Windows Update, and Store access; this is separate from guest networking. |
| `0x80070005` with a desktop mapping | Use a dedicated guest subdirectory such as `C:\Input`; avoid mapping over the guest Desktop root. |

For policy conflicts, consult [WindowsSandbox Policy CSP](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-windowssandbox). Relevant Group Policy is under **Computer Configuration > Administrative Templates > Windows Components > Windows Sandbox**; the policy registry key is `HKLM:\SOFTWARE\Policies\Microsoft\Windows\Sandbox`. Read applicable settings without clearing or bypassing organization policy.

Report what was created, what actually ran, the observed outcome, and where results were saved. Distinguish configuration validation from a successful guest launch and from successful application behavior.
