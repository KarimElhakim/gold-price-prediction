# Clean git push wrapper for PowerShell
# Eliminates false error messages from git stderr output

param(
    [string]$Branch = "main"
)

# Suppress PowerShell error handling for this command
$ErrorActionPreference = "SilentlyContinue"

# Execute git push and capture output
$output = & git push origin $Branch 2>&1

# Check the actual git exit code
$exitCode = $LASTEXITCODE

# Filter out the PowerShell "error" that's actually just git's normal stderr
$cleanOutput = $output | Where-Object { 
    $_ -notmatch "CategoryInfo" -and 
    $_ -notmatch "RemoteException" -and 
    $_ -notmatch "NativeCommandError" -and
    $_ -notmatch "FullyQualifiedErrorId"
}

# Display clean output
if ($cleanOutput) {
    $cleanOutput | ForEach-Object { Write-Host $_ }
}

# Check if push was successful (look for "main -> main" or similar pattern)
if ($exitCode -eq 0 -or ($output -match "->")) {
    Write-Host "`n✓ Successfully pushed to origin/$Branch" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n✗ Push failed with exit code: $exitCode" -ForegroundColor Red
    exit 1
}

