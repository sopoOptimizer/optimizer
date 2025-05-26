$powerPlanName = "SOPOptimizer - Uso Diario"
$powerPlanDesc = "Pla optimitzat per ús diari."

# Comprova si ja existeix
$existingPlan = powercfg -list | Select-String $powerPlanName
if ($existingPlan) {
    if ($existingPlan -match "([a-fA-F0-9\-]{36})") {
        $guid = $matches[1]
        powercfg -setactive $guid
        Write-Host "Pla d'energia ja existent activat." -ForegroundColor Green
    } else {
        Write-Host "No s'ha pogut extreure el GUID del pla existent." -ForegroundColor Red
    }
} else {
    # Duplica el pla Equilibrat i posa-li nom i descripció
    $guid = (powercfg -duplicatescheme SCHEME_BALANCED).Trim()
    if ($guid -match "([a-fA-F0-9\-]{36})") {
        $guid = $matches[1]
        powercfg -changename $guid $powerPlanName $powerPlanDesc
        powercfg -setactive $guid
        Write-Host "Pla d'energia creat i activat correctament." -ForegroundColor Green
    } else {
        Write-Host "No s'ha pogut crear el pla d'energia." -ForegroundColor Red
    }
}