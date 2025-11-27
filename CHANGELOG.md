# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- Gold price prediction notebook with machine learning models
- Kaggle dataset integration for historical gold price data
- Google RSS news feed integration with sentiment analysis
- Alpha Vantage API integration for real-time gold prices
- News sentiment analysis with gold-specific price direction indicators
- Keyword detection system for identifying price rise/fall signals
- Random Forest models for direction prediction (up/down classification)
- Random Forest regressor for price range prediction
- Comprehensive data visualization with 4-panel dashboard
- Feature engineering with technical indicators (moving averages, volatility)
- News sentiment aggregation with combined scoring

### Changed
- Initial release with production-ready code structure

### Technical Details
- **Data Sources**: Kaggle gold price dataset, Google RSS feeds, Alpha Vantage API
- **ML Models**: RandomForestClassifier (direction), RandomForestRegressor (price range)
- **Features**: Historical prices, moving averages, volatility, news sentiment, API prices
- **Dependencies**: pandas, numpy, scikit-learn, matplotlib, seaborn, feedparser, textblob

