# Simple clean push script
# Usage: .\push.ps1 [commit-message]

param([string]$Message = "")

$ErrorActionPreference = "Continue"

# Add all changes
git add . 2>$null

# Commit if message provided
if ($Message) {
    git commit -m $Message 2>$null
}

# Push with clean error handling
$result = git push origin main 2>&1 | Out-String

# Check for success indicators
if ($result -match "->" -or $LASTEXITCODE -eq 0) {
    Write-Host "✓ Successfully pushed to GitHub" -ForegroundColor Green
} else {
    Write-Host "Push failed. Error details:" -ForegroundColor Red
    Write-Host $result -ForegroundColor Red
}

