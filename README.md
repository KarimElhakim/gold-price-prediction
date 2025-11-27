# Gold Price Prediction

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Machine learning project that predicts gold price direction (up/down) and price range using historical data, news sentiment analysis, and real-time market data.

## Overview

This notebook integrates multiple data sources to build predictive models:

- Historical gold price data from Kaggle
- Google RSS news feeds analyzed for sentiment
- Real-time gold price APIs for current market conditions

The models predict both the direction of price movement (classification) and the expected price range (regression).

## Data Sources

1. Historical price data: Kaggle gold price prediction dataset
2. News sentiment: Google RSS feeds with natural language processing and price direction indicators
3. Real-time prices: Alpha Vantage API for current gold market prices

## Features

- Direction prediction model (up/down classification)
- Price range estimation model (regression)
- News sentiment integration
- Real-time API data integration
- Comprehensive data visualizations

## Setup

Configure your Kaggle API token in the Configuration section of the notebook. Optional Alpha Vantage API key can be added for enhanced price data reliability.

## Usage

### Option 1: Google Colab (Recommended for Quick Start)

Open this notebook in Google Colab directly from GitHub. All required packages are installed automatically in the first cell.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KarimElhakim/gold-price-prediction/blob/main/gold_price_prediction.ipynb)

### Option 2: Local Development

To run the notebook locally on your machine:

1. **Quick Setup (Automated)**:
   - **Windows**: Run `setup_local.ps1` in PowerShell
   - **macOS/Linux**: Run `bash setup_local.sh`

2. **Manual Setup**:
   - Install Python 3.8+ and create a virtual environment
   - Install dependencies: `pip install -r requirements.txt`
   - Download TextBlob corpora: `python -m textblob.download_corpora`
   - Start Jupyter: `jupyter notebook`

See [SETUP.md](SETUP.md) for detailed installation instructions and troubleshooting.
