#!/bin/bash
# Bash Script for Local Setup on macOS/Linux
# Run this script to automatically set up the environment

echo "=== Gold Price Prediction - Local Setup ==="
echo ""

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "Found: $PYTHON_VERSION"
    
    # Check Python version (need 3.8+)
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        echo "ERROR: Python 3.8 or higher is required!"
        exit 1
    fi
else
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "Virtual environment created successfully!"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo ""
echo "Installing required packages (this may take a few minutes)..."
pip install -r requirements.txt

# Download TextBlob corpora
echo ""
echo "Downloading TextBlob corpora..."
python -m textblob.download_corpora

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, feedparser, requests, bs4, textblob, kagglehub, jupyter; print('✓ All packages installed successfully!')"

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start Jupyter: jupyter notebook"
echo "3. Open gold_price_prediction.ipynb"
echo "4. Update API keys in the Configuration section"
echo ""

