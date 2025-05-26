Write-Host "Creant i activant el pla d'energia per a treball..." -ForegroundColor Cyan

# Nom i descripció del pla
$powerPlanName = "SOPOptimizer - Trabajo"
$powerPlanDesc = "Pla optimitzat per a treball."

# Busca plans existents amb el mateix nom i elimina'ls
$existing = powercfg /list | Select-String $powerPlanName
if ($existing) {
    $guid = ($existing -split '\s+')[3]
    Write-Host "Eliminant pla existent: $guid"
    powercfg /delete $guid
}    

$existingPlan = powercfg -list | Select-String $powerPlanName
if ($existingPlan) {
    if ($existingPlan -match "([a-fA-F0-9\-]{36})") {
        $guid = $matches[1]
        powercfg -setactive $guid
        Write-Host "Pla d'energia per a treball ja existent activat." -ForegroundColor Green
    } else {
        Write-Host "No s'ha pogut extreure el GUID del pla existent." -ForegroundColor Red
    }
} else {
    $guid = (powercfg -duplicatescheme SCHEME_BALANCED).Trim()
    if ($guid -match "([a-fA-F0-9\-]{36})") {
        $guid = $matches[1]
        powercfg -changename $guid $powerPlanName $powerPlanDesc
        powercfg -setactive $guid
        Write-Host "Pla d'energia per a treball creat i activat correctament." -ForegroundColor Green
    } else {
        Write-Host "No s'ha pogut crear el pla d'energia per a treball." -ForegroundColor Red
    }
}
