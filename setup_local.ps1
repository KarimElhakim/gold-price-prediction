# PowerShell Script for Local Setup on Windows
# Run this script to automatically set up the environment

Write-Host "=== Gold Price Prediction - Local Setup ===" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    
    # Check Python version (need 3.8+)
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Host "ERROR: Python 3.8 or higher is required!" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host ""
Write-Host "Installing required packages (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt

# Download TextBlob corpora
Write-Host ""
Write-Host "Downloading TextBlob corpora..." -ForegroundColor Yellow
python -m textblob.download_corpora

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, feedparser, requests, bs4, textblob, kagglehub, jupyter; print('✓ All packages installed successfully!')"

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate the virtual environment: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Start Jupyter: jupyter notebook" -ForegroundColor White
Write-Host "3. Open gold_price_prediction.ipynb" -ForegroundColor White
Write-Host "4. Update API keys in the Configuration section" -ForegroundColor White
Write-Host ""

