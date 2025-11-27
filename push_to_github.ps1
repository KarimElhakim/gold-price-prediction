# GitHub Push Script - Clean output version
# This script handles git push with proper error suppression

param(
    [string]$Branch = "main",
    [string]$Message = ""
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Pushing to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check git status
Write-Host "Checking git status..." -ForegroundColor Yellow
$status = git status --short 2>&1 | Out-String
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes to commit." -ForegroundColor Yellow
    exit 0
}

# Add all changes
Write-Host "Staging changes..." -ForegroundColor Yellow
$addOutput = git add . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to stage changes" -ForegroundColor Red
    exit 1
}

# Commit if message provided
if (-not [string]::IsNullOrWhiteSpace($Message)) {
    Write-Host "Committing changes..." -ForegroundColor Yellow
    $commitOutput = git commit -m $Message 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Commit may have failed or nothing to commit" -ForegroundColor Yellow
    }
}

# Push to GitHub
Write-Host "Pushing to origin/$Branch..." -ForegroundColor Yellow
$pushOutput = git push origin $Branch 2>&1 | Tee-Object -Variable pushResult

# Check actual exit code (not PowerShell's interpretation)
$gitExitCode = $LASTEXITCODE

if ($gitExitCode -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS: Pushed to GitHub successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Branch: $Branch" -ForegroundColor Cyan
    Write-Host "Repository: https://github.com/KarimElhakim/gold-price-prediction" -ForegroundColor Cyan
    Write-Host ""
    exit 0
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Push failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host $pushOutput -ForegroundColor Red
    exit 1
}

