# windows_update.ps1
Write-Output "Buscando actualizaciones de Windows Update..."
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software'")
if ($SearchResult.Updates.Count -eq 0) {
    Write-Output "No hay actualizaciones pendientes."
} else {
    Write-Output "Actualizaciones encontradas: $($SearchResult.Updates.Count)"
    foreach ($update in $SearchResult.Updates) {
        Write-Output "- $($update.Title)"
    }
}