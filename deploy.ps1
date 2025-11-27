# Gold Price Prediction - Deployment Script
# Simple script to commit and push changes to GitHub
# Usage: .\deploy.ps1 [commit-message]

param(
    [Parameter(Mandatory=$false)]
    [string]$Message = "chore: update project files"
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Gold Price Prediction - Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a git repository
if (-not (Test-Path .git)) {
    Write-Host "Error: Not a git repository" -ForegroundColor Red
    exit 1
}

# Stage all changes
Write-Host "Staging changes..." -ForegroundColor Yellow
git add . 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Failed to stage some files" -ForegroundColor Yellow
}

# Check if there are changes to commit
$status = git status --short 2>$null
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes to commit" -ForegroundColor Green
} else {
    # Commit changes
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m $Message 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Commit created: $Message" -ForegroundColor Green
    } else {
        Write-Host "Warning: Commit may have failed or nothing to commit" -ForegroundColor Yellow
    }
}

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
$output = git push origin main 2>&1 | Out-String

# Check for success
if ($LASTEXITCODE -eq 0 -or $output -match "->") {
    Write-Host ""
    Write-Host "✓ Successfully deployed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/KarimElhakim/gold-price-prediction" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Deployment failed" -ForegroundColor Red
    Write-Host "Check the output above for details" -ForegroundColor Yellow
    exit 1
}

