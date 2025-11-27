# Local Setup Guide

This guide will help you set up the environment to run the Gold Price Prediction notebook locally on your machine.

## Prerequisites

- **Python 3.8 or higher** (Python 3.9+ recommended)
- **pip** (Python package installer)
- **Git** (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/KarimElhakim/gold-price-prediction.git
cd gold-price-prediction
```

### 2. Create a Virtual Environment (Recommended)

#### Windows:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# If activation script execution is disabled, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

Once your virtual environment is activated:

```bash
# Install all required packages
pip install -r requirements.txt

# Or install directly
pip install pandas numpy scikit-learn matplotlib seaborn kagglehub feedparser requests beautifulsoup4 textblob jupyter ipykernel notebook ipython
```

### 4. Additional Setup for TextBlob

TextBlob requires additional data for NLP features:

```bash
python -m textblob.download_corpora
```

This downloads necessary corpora for sentiment analysis.

### 5. Configure API Keys

Open `gold_price_prediction.ipynb` and update the Configuration section (Cell 2) with your API keys:

```python
KAGGLE_API_TOKEN = "your_kaggle_token_here"
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_key_here"
```

#### Getting API Keys:

1. **Kaggle API Token**:
   - Go to https://www.kaggle.com/account
   - Scroll to "API" section
   - Click "Create New Token"
   - Save the `kaggle.json` file or copy the token

2. **Alpha Vantage API Key**:
   - Go to https://www.alphavantage.co/support/#api-key
   - Fill out the form to get a free API key

### 6. Launch Jupyter Notebook

```bash
# Start Jupyter Notebook server
jupyter notebook

# Or use JupyterLab for a better experience
pip install jupyterlab
jupyter lab
```

The notebook will open in your default web browser.

### 7. Run the Notebook

1. Open `gold_price_prediction.ipynb` from the Jupyter interface
2. Run cells sequentially from top to bottom
3. Wait for dataset download on first run (Cell 5)

## Troubleshooting

### Issue: `pip` command not found
**Solution**: Install Python with pip included, or use `python -m pip` instead of `pip`

### Issue: Virtual environment activation fails (Windows)
**Solution**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: ModuleNotFoundError after installation
**Solution**: 
- Make sure your virtual environment is activated
- Reinstall packages: `pip install --upgrade -r requirements.txt`

### Issue: TextBlob sentiment analysis fails
**Solution**: Download corpora: `python -m textblob.download_corpora`

### Issue: Kaggle dataset download fails
**Solution**: 
- Verify your Kaggle API token is correct
- Check internet connection
- Ensure `kagglehub` package is installed

### Issue: Alpha Vantage API rate limit exceeded
**Solution**: 
- Free tier allows 5 API calls per minute
- Wait 1 minute between requests
- Consider upgrading to premium API tier

## Alternative: Using Conda

If you prefer using Conda/Miniconda:

```bash
# Create conda environment
conda create -n gold-price-prediction python=3.9

# Activate environment
conda activate gold-price-prediction

# Install packages
conda install pandas numpy scikit-learn matplotlib seaborn jupyter
pip install kagglehub feedparser requests beautifulsoup4 textblob

# Download TextBlob corpora
python -m textblob.download_corpora
```

## System Requirements

- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: ~500MB for packages + dataset storage
- **Internet**: Required for dataset download and API calls

## Verification

To verify your installation is working correctly:

```python
# Run this in a Python shell or notebook
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import feedparser
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import kagglehub
import jupyter

print("All packages imported successfully!")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Scikit-learn version: {sklearn.__version__}")
```

## Next Steps

1. Run the notebook cells in order
2. Explore the visualizations
3. Experiment with different model parameters
4. Customize the news analysis keywords

For more information, see:
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Release information

