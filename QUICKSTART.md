# Quick Start Guide

Get up and running with the Gold Price Prediction notebook in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Internet connection (for downloading packages and dataset)

## Option 1: Automated Setup (Recommended)

### Windows
```powershell
# Run the setup script
.\setup_local.ps1
```

### macOS/Linux
```bash
# Make script executable and run
chmod +x setup_local.sh
./setup_local.sh
```

The script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Download TextBlob corpora
- ✅ Verify installation

## Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Download TextBlob data
python -m textblob.download_corpora
```

## Launch Jupyter

```bash
# Make sure virtual environment is activated, then:
jupyter notebook
```

The notebook will open in your browser automatically.

## Configure API Keys

Before running the notebook, update the Configuration cell (Cell 2) with your API keys:

1. **Kaggle API Token**: Get from https://www.kaggle.com/account
2. **Alpha Vantage API Key**: Get from https://www.alphavantage.co/support/#api-key

## Run the Notebook

1. Open `gold_price_prediction.ipynb` in Jupyter
2. Run cells sequentially (Cell → Run All)
3. Wait for dataset download (first run only)

## Troubleshooting

**Can't activate virtual environment?**
- Windows: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try activating again

**Packages not found?**
- Make sure virtual environment is activated
- Reinstall: `pip install --upgrade -r requirements.txt`

**TextBlob errors?**
- Run: `python -m textblob.download_corpora`

## What's Next?

- 📊 Explore the visualizations
- 🔧 Experiment with model parameters
- 📰 Customize news analysis keywords
- 📈 Add your own features

For detailed information, see [SETUP.md](SETUP.md).

