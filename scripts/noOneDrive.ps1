$OneDrivePath = $($env:OneDrive)
Write-Host "Removing OneDrive"
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\OneDriveSetup.exe"
if (Test-Path $regPath) {
    $OneDriveUninstallString = Get-ItemPropertyValue "$regPath" -Name "UninstallString"
    $OneDriveExe, $OneDriveArgs = $OneDriveUninstallString.Split(" ")
    Start-Process -FilePath $OneDriveExe -ArgumentList "$OneDriveArgs /silent" -NoNewWindow -Wait
} else {
    Write-Host "Onedrive dosn't seem to be installed anymore" -ForegroundColor Red
    return
}

if (-not (Test-Path $regPath)) {
    Write-Host "Copy downloaded Files from the OneDrive Folder to Root UserProfile"
    Start-Process -FilePath powershell -ArgumentList "robocopy '$($OneDrivePath)' '$($env:USERPROFILE.TrimEnd())\' /mov /e /xj" -NoNewWindow -Wait

    Write-Host "Removing OneDrive leftovers"
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:localappdata\Microsoft\OneDrive"
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:localappdata\OneDrive"
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:programdata\Microsoft OneDrive"
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:systemdrive\OneDriveTemp"
    reg delete "HKEY_CURRENT_USER\Software\Microsoft\OneDrive" -f
    
    If ((Get-ChildItem "$OneDrivePath" -Recurse | Measure-Object).Count -eq 0) {
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$OneDrivePath"
    }

    Write-Host "Remove Onedrive from explorer sidebar"
    Set-ItemProperty -Path "HKCR:\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}" -Name "System.IsPinnedToNameSpaceTree" -Value 0
    Set-ItemProperty -Path "HKCR:\Wow6432Node\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}" -Name "System.IsPinnedToNameSpaceTree" -Value 0

    Write-Host "Removing run hook for new users"
    reg load "hku\Default" "C:\Users\Default\NTUSER.DAT"
    reg delete "HKEY_USERS\Default\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "OneDriveSetup" /f
    reg unload "hku\Default"

    Write-Host "Removing startmenu entry"
    Remove-Item -Force -ErrorAction SilentlyContinue "$env:userprofile\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\OneDrive.lnk"

    Write-Host "Removing scheduled task"
    Get-ScheduledTask -TaskPath '\' -TaskName 'OneDrive*' -ea SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

    Write-Host "Shell Fixing"
    # Restaurar ubicaciones por defecto de carpetas del sistema
    $shellFolders = @{
        "AppData" = "$env:userprofile\AppData\Roaming"
        "Cache" = "$env:userprofile\AppData\Local\Microsoft\Windows\INetCache"
        "Cookies" = "$env:userprofile\AppData\Local\Microsoft\Windows\INetCookies"
        "Favorites" = "$env:userprofile\Favorites"
        "History" = "$env:userprofile\AppData\Local\Microsoft\Windows\History"
        "Local AppData" = "$env:userprofile\AppData\Local"
        "My Music" = "$env:userprofile\Music"
        "My Video" = "$env:userprofile\Videos"
        "NetHood" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Network Shortcuts"
        "PrintHood" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Printer Shortcuts"
        "Programs" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
        "Recent" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Recent"
        "SendTo" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\SendTo"
        "Start Menu" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Start Menu"
        "Startup" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        "Templates" = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Templates"
        "{374DE290-123F-4565-9164-39C4925E467B}" = "$env:userprofile\Downloads"
        "Desktop" = "$env:userprofile\Desktop"
        "My Pictures" = "$env:userprofile\Pictures"
        "Personal" = "$env:userprofile\Documents"
        "{F42EE2D3-909F-4907-8871-4C22FC0BF756}" = "$env:userprofile\Documents"
        "{0DDD015D-B06C-45D5-8C4C-F59713854639}" = "$env:userprofile\Pictures"
    }

    foreach ($key in $shellFolders.Keys) {
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" -Name $key -Value $shellFolders[$key] -Type ExpandString
    }

    Write-Host "Restarting explorer"
    taskkill.exe /F /IM "explorer.exe"
    Start-Process "explorer.exe"

    Write-Host "Waiting for explorer to complete loading"
    Write-Host "Please Note - The OneDrive folder at $OneDrivePath may still have items in it. You must manually delete it, but all the files should already be copied to the base user folder."
    Write-Host "If there are Files missing afterwards, please Login to Onedrive.com and Download them manually" -ForegroundColor Yellow
    Start-Sleep 5
} else {
    Write-Host "Something went Wrong during the Unistallation of OneDrive" -ForegroundColor Red
}
