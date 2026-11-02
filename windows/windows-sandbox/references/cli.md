# Windows Sandbox CLI

Read this for command automation. Microsoft documents `wsb` for Windows 11 24H2 onward; verify the installed executable and each command's help. Fall back to a `.wsb` launch when unavailable. See the [official CLI reference](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-cli).

```powershell
wsb --help
wsb start --help
wsb exec --help
```

Pass XML text to `--config`, not a filename. Capture the returned ID; never select an unrelated session:

```powershell
wsb start --config (Get-Content -LiteralPath $configPath -Raw)
wsb list
wsb connect --id $sandboxId
wsb exec --id $sandboxId --command 'C:\Input\TestApp.exe' --run-as ExistingLogin
wsb share --id $sandboxId --host-path $outputPath --sandbox-path 'C:\Output' --allow-write
wsb ip --id $sandboxId
wsb stop --id $sandboxId
```

`ExistingLogin` requires an active guest login; connect first. Use `System` only when required. `exec` returns an exit code but currently provides no process stdout/stderr; collect guest-written logs through a dedicated output mapping. `share` is read-only unless `--allow-write` is specified. `--raw` provides JSON; confirm placement and schema locally. Stop only the job's session after collecting results. The lines above demonstrate separate operations, not an unconditional sequence.
