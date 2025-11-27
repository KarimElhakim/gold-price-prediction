# Gold Price Prediction - Full Python Application

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)

Full-featured Python application for predicting gold price direction (up/down) and price range using machine learning, news sentiment analysis, and real-time market data.

## Overview

This is a complete Python application (not just a notebook) that provides:
- **Real-time gold price predictions** using trained ML models
- **Live dashboard** for monitoring and analysis
- **Automated data fetching** from multiple sources
- **Model training and persistence**
- **News sentiment analysis** with price impact indicators

## Architecture

```
gold-price-prediction/
├── app/                    # Application package
│   ├── core/              # Core application logic
│   ├── data/              # Data fetching modules
│   ├── features/          # Feature engineering
│   ├── models/            # ML models
│   ├── utils/             # Utilities
│   └── config.py          # Configuration
├── models/                 # Saved model files
├── main.py                # Main entry point
├── live_dashboard.py      # Streamlit dashboard
└── requirements.txt       # Dependencies
```

## Features

- **Direction Prediction**: Predicts whether gold price will go UP or DOWN
- **Price Range Prediction**: Estimates the expected price change amount
- **Real-time Data**: Live gold prices from GoldAPI.io
- **News Analysis**: Intelligent news fetching with sentiment and price impact analysis
- **Live Dashboard**: Interactive web dashboard with real-time updates
- **Model Persistence**: Save and load trained models

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KarimElhakim/gold-price-prediction.git
   cd gold-price-prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (optional, defaults provided):
   ```bash
   export KAGGLE_API_TOKEN="your-kaggle-token"
   export GOLDAPI_API_KEY="your-goldapi-key"
   ```

### Running the Application

#### Option 1: Run Dashboard (Recommended)
```bash
python run_app.py dashboard
# or
streamlit run live_dashboard.py
```

#### Option 2: Full Cycle (Train + Predict)
```bash
python main.py --mode full
```

#### Option 3: Train Models Only
```bash
python main.py --mode train
```

#### Option 4: Make Prediction Only
```bash
python main.py --mode predict
```

## Usage

### Training Models

Models are automatically trained on first run, or you can train explicitly:

```python
from app.core import GoldPriceApp

app = GoldPriceApp()
app.load_historical_data()
app.process_data()
metrics = app.train_models()
print(f"Accuracy: {metrics['direction']['accuracy']:.2%}")
```

### Making Predictions

```python
from app.core import GoldPriceApp

app = GoldPriceApp()
app.load_trained_models()  # Load existing models

# Get latest news and current price
news = app.get_latest_news()
current_price = app.get_current_price()

# Make prediction
prediction = app.predict(news_data=news, current_price=current_price)
print(f"Direction: {prediction['direction']}")
print(f"Confidence: {prediction['confidence']:.1f}%")
print(f"Expected Change: ${prediction['price_change']:.2f}")
```

### Using Individual Components

```python
from app.data import GoldAPIClient, NewsFetcher
from app.models import PricePredictor

# Fetch current price
api_client = GoldAPIClient()
price_data = api_client.get_current_price()

# Fetch and analyze news
news_fetcher = NewsFetcher()
news = news_fetcher.get_all_relevant_gold_news()
news_analysis = news_fetcher.analyze_news_impact(news)
```

## Dashboard

The live dashboard provides:
- Real-time gold price updates
- Latest impactful news with sentiment analysis
- Model predictions with confidence scores
- Interactive price charts
- Performance metrics

Access at: `http://localhost:8501`

## Data Sources

1. **Historical Data**: Kaggle gold price prediction dataset
2. **News Sentiment**: Google RSS feeds with NLP analysis
3. **Real-time Prices**: GoldAPI.io for live XAU/USD spot prices

## Configuration

Edit `app/config.py` or set environment variables:

```python
KAGGLE_API_TOKEN = "your-token"
GOLDAPI_API_KEY = "your-key"
```

## Model Details

- **Direction Model**: Random Forest Classifier
- **Range Model**: Random Forest Regressor
- **Features**: 16 features combining historical, news, and API data
- **Training**: Models saved to `models/` directory

## Development

### Project Structure

- `app/core/gold_price_app.py` - Main application class
- `app/data/` - Data fetching (Kaggle, GoldAPI, News)
- `app/models/` - ML models (Direction, Range, Predictor)
- `app/features/` - Feature engineering
- `app/config.py` - Configuration management

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests (when added)
pytest tests/
```

## Deployment

### Local Deployment

```bash
# Run dashboard
python run_app.py dashboard
```

### Production Deployment

1. **Train models first:**
   ```bash
   python main.py --mode train
   ```

2. **Deploy dashboard** using Streamlit Cloud, Heroku, or Docker

3. **Set environment variables** for API keys

## Requirements

See `requirements.txt` for full list. Key dependencies:
- pandas, numpy
- scikit-learn
- streamlit, plotly
- feedparser, requests
- kagglehub
- textblob, joblib

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
