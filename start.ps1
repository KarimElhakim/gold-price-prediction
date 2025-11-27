# Start the Gold Price Prediction Application (Windows)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Gold Price Prediction Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Error: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host "Python found: $($python.Version)" -ForegroundColor Green
Write-Host ""

# Install dependencies if needed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
python -c "import pandas, numpy, sklearn, streamlit, plotly" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

# Setup directories
Write-Host "Setting up directories..." -ForegroundColor Yellow
python -c "from app.config import Config; Config.setup_directories()"

Write-Host ""
Write-Host "Starting dashboard..." -ForegroundColor Green
Write-Host "Dashboard will open at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start Streamlit
python -m streamlit run live_dashboard.py --server.port 8501

