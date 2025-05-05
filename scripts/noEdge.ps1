function Uninstall-EdgeBrowser {

    $msedgeProcess = Get-Process -Name "msedge" -ErrorAction SilentlyContinue
    $widgetsProcess = Get-Process -Name "widgets" -ErrorAction SilentlyContinue
    
    if ($msedgeProcess) {
        Stop-Process -Name "msedge" -Force
    } else {
        Write-Output "[INFO] msedge process is not running."
    }
    
    if ($widgetsProcess) {
        Stop-Process -Name "widgets" -Force
    } else {
        Write-Output "[INFO] widgets process is not running."
    }

    function Uninstall-Process {
        param (
            [Parameter(Mandatory = $true)]
            [string]$Key
        )

        $originalNation = [microsoft.win32.registry]::GetValue('HKEY_USERS\.DEFAULT\Control Panel\International\Geo', 'Nation', [Microsoft.Win32.RegistryValueKind]::String)
        [microsoft.win32.registry]::SetValue('HKEY_USERS\.DEFAULT\Control Panel\International\Geo', 'Nation', 68, [Microsoft.Win32.RegistryValueKind]::String) | Out-Null

        $fileName = "IntegratedServicesRegionPolicySet.json"
        $pathISRPS = [Environment]::SystemDirectory + "\" + $fileName
        $aclISRPS = Get-Acl -Path $pathISRPS
        $aclISRPSBackup = [System.Security.AccessControl.FileSecurity]::new()
        $aclISRPSBackup.SetSecurityDescriptorSddlForm($acl.Sddl)
        
        if (Test-Path -Path $pathISRPS) {
            try {
                $admin = [System.Security.Principal.NTAccount]$(New-Object System.Security.Principal.SecurityIdentifier('S-1-5-32-544')).Translate([System.Security.Principal.NTAccount]).Value
                $aclISRPS.SetOwner($admin)
                $rule = New-Object System.Security.AccessControl.FileSystemAccessRule($admin, 'FullControl', 'Allow')
                $aclISRPS.AddAccessRule($rule)
                Set-Acl -Path $pathISRPS -AclObject $aclISRPS
                Rename-Item -Path $pathISRPS -NewName ($fileName + '.bak') -Force
            }
            catch {
                Write-Error "[Edge] Failed to set owner for $pathISRPS"
            }
        }

        $baseKey = 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate'
        $registryPath = $baseKey + '\ClientState\' + $Key

        if (!(Test-Path -Path $registryPath)) {
            Write-Host "[Edge] Registry key not found: $registryPath"
            return
        }

        Remove-ItemProperty -Path $registryPath -Name "experiment_control_labels" -ErrorAction SilentlyContinue | Out-Null

        $uninstallString = (Get-ItemProperty -Path $registryPath).UninstallString
        $uninstallArguments = (Get-ItemProperty -Path $registryPath).UninstallArguments

        if ([string]::IsNullOrEmpty($uninstallString) -or [string]::IsNullOrEmpty($uninstallArguments)) {
            Write-Host "[Edge] Cannot find uninstall methods"
            return
        }

        $uninstallArguments += " --force-uninstall --delete-profile"

        if (!(Test-Path -Path $uninstallString)) {
            Write-Host "[Edge] setup.exe not found at: $uninstallString"
            return
        }
        Start-Process -FilePath $uninstallString -ArgumentList $uninstallArguments -Wait -NoNewWindow

        if (Test-Path -Path ($pathISRPS + '.bak')) {
            Rename-Item -Path ($pathISRPS + '.bak') -NewName $fileName -Force
            Set-Acl -Path $pathISRPS -AclObject $aclISRPSBackup
        }

        [microsoft.win32.registry]::SetValue('HKEY_USERS\.DEFAULT\Control Panel\International\Geo', 'Nation', $originalNation, [Microsoft.Win32.RegistryValueKind]::String) | Out-Null

        if ((Get-ItemProperty -Path $baseKey).IsEdgeStableUninstalled -eq 1) {
            Write-Host "[Edge] Edge Stable has been successfully uninstalled"
        }
    }

    function Uninstall-Edge {
        Remove-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" -Name "NoRemove" -ErrorAction SilentlyContinue | Out-Null
        [microsoft.win32.registry]::SetValue("HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdateDev", "AllowUninstall", 1, [Microsoft.Win32.RegistryValueKind]::DWord) | Out-Null
        Uninstall-Process -Key '{56EB18F8-B008-4CBD-B6D2-8C97FE7E9062}'

        @( "$env:ProgramData\Microsoft\Windows\Start Menu\Programs",
           "$env:PUBLIC\Desktop",
           "$env:USERPROFILE\Desktop" ) | ForEach-Object {
            $shortcutPath = Join-Path -Path $_ -ChildPath "Microsoft Edge.lnk"
            if (Test-Path -Path $shortcutPath) {
                Remove-Item -Path $shortcutPath -Force
            }
        }
    }

    Uninstall-Edge
    Write-Host "[SUCCESS] Microsoft Edge ha sido desinstalado correctamente" -ForegroundColor Green
}

Uninstall-EdgeBrowser
