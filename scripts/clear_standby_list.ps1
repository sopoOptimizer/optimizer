# Vacía la Standby List (memoria caché) en Windows. Requiere ejecutar como administrador.
$signature = @'
[DllImport("ntdll.dll")]
public static extern uint NtSetSystemInformation(int InfoClass, IntPtr Info, int Length);
'@
Add-Type -MemberDefinition $signature -Name 'Win32' -Namespace 'Win32Functions'
[Win32Functions.Win32]::NtSetSystemInformation(0x50, [IntPtr]::Zero, 0)
Write-Host "Standby List vaciada."
