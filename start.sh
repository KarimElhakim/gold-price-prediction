#!/bin/bash
# Start the Gold Price Prediction Application (Linux/Mac)

echo "========================================"
echo "Gold Price Prediction Application"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Install dependencies if needed
echo "Checking dependencies..."
python3 -c "import pandas, numpy, sklearn, streamlit, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
fi

# Setup directories
echo "Setting up directories..."
python3 -c "from app.config import Config; Config.setup_directories()"

echo ""
echo "Starting dashboard..."
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

# Start Streamlit
python3 -m streamlit run live_dashboard.py --server.port 8501

