# Script PowerShell para activar el modo oscuro en Windows

# Modifica el registro para usar tema oscuro en apps y sistema
try {
    Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Type DWord -Value 0 -ErrorAction Stop
    Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "SystemUsesLightTheme" -Type DWord -Value 0 -ErrorAction Stop
    Write-Host "Modo oscuro activado correctamente."
} catch {
    Write-Error "Error al activar el modo oscuro: $_"
}
