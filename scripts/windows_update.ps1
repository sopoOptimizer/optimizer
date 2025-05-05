# Script PowerShell para buscar actualizaciones de Windows Update
Write-Host "Buscando actualizaciones de Windows Update..."
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software'")
if ($SearchResult.Updates.Count -eq 0) {
    Write-Host "No hay actualizaciones pendientes."
} else {
    Write-Host "Actualizaciones encontradas: $($SearchResult.Updates.Count)"
    foreach ($update in $SearchResult.Updates) {
        Write-Host "- $($update.Title)"
    }
}
