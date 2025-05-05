# Desactivar Game Bar y grabación para el usuario actual

Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR' -Name 'AppCaptureEnabled' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR' -Name 'GameDVR_Enabled' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\System\\GameConfigStore' -Name 'GameDVR_Enabled' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'GameBarEnabled' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'AllowAutoGameMode' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'AutoGameModeEnabled' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'ShowStartupPanel' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'UseNexusForGameBarEnabled' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'GamePanelStartupTipIndex' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'GamePanelStartupTipVisible' -Type DWord -Value 0
Set-ItemProperty -Path 'HKCU:\\SOFTWARE\\Microsoft\\GameBar' -Name 'OpenGameBarOnGameLaunch' -Type DWord -Value 0

