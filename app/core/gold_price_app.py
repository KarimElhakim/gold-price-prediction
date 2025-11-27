"""
Main application class for Gold Price Prediction
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

from app.config import Config
from app.data import KaggleDataFetcher, GoldAPIClient, NewsFetcher
from app.features import FeatureEngineer
from app.models import PricePredictor


class GoldPriceApp:
    """Main application class"""
    
    def __init__(self):
        self.config = Config
        self.data_fetcher = KaggleDataFetcher()
        self.gold_api = GoldAPIClient()
        self.news_fetcher = NewsFetcher()
        self.feature_engineer = FeatureEngineer()
        self.predictor = PricePredictor()
        
        self.historical_data: Optional[pd.DataFrame] = None
        self.processed_data: Optional[pd.DataFrame] = None
        self.models_trained: bool = False
    
    def load_historical_data(self) -> pd.DataFrame:
        """Load and process historical data from Kaggle"""
        print("Loading historical data from Kaggle...")
        self.historical_data = self.data_fetcher.get_data()
        return self.historical_data
    
    def process_data(self) -> pd.DataFrame:
        """Process historical data and create features"""
        if self.historical_data is None:
            self.load_historical_data()
        
        print("Processing data and creating features...")
        self.processed_data = self.feature_engineer.create_price_features(self.historical_data)
        return self.processed_data
    
    def train_models(self) -> Dict:
        """Train the prediction models"""
        if self.processed_data is None:
            self.process_data()
        
        # Prepare features and targets
        feature_names = self.feature_engineer.get_feature_names()
        
        # Create feature matrix for all historical data
        X_list = []
        y_direction_list = []
        y_range_list = []
        
        for idx in range(len(self.processed_data)):
            row = self.processed_data.iloc[idx]
            if pd.isna(row.get('next_direction')):
                continue
            
            # Create feature matrix for this row (without news/API for historical training)
            features = []
            
            # Historical price features
            price_features = [
                'price_change', 'price_change_pct', 'price_ma_7', 'price_ma_30',
                'price_std_7', 'volatility', 'momentum_7', 'momentum_30'
            ]
            
            for feature in price_features:
                if feature in self.processed_data.columns:
                    val = row[feature]
                    features.append(float(val) if not pd.isna(val) else 0.0)
                else:
                    features.append(0.0)
            
            # News features (0 for historical training)
            features.extend([0.0, 0.0, 0.0, 0.0])
            
            # API features (0 for historical training)
            features.extend([0.0, 0.0, 0.0, 0.0])
            
            X_list.append(features)
            y_direction_list.append(int(row['next_direction']))
            y_range_list.append(float(row.get('next_price_change', 0.0)))
        
        X = np.array(X_list)
        y_direction = np.array(y_direction_list)
        y_range = np.array(y_range_list)
        
        # Train models
        metrics = self.predictor.train(X, y_direction, y_range, feature_names)
        self.models_trained = True
        
        # Save models
        self.predictor.save_models(Config.MODELS_DIR)
        
        return metrics
    
    def load_trained_models(self):
        """Load pre-trained models"""
        direction_model_path = Config.MODELS_DIR / "direction_model.pkl"
        range_model_path = Config.MODELS_DIR / "range_model.pkl"
        
        if not direction_model_path.exists() or not range_model_path.exists():
            raise FileNotFoundError("Models not found. Train models first.")
        
        self.predictor.load_models(Config.MODELS_DIR)
        self.models_trained = True
    
    def predict(
        self,
        news_data: Optional[pd.DataFrame] = None,
        current_price: Optional[Dict] = None
    ) -> Dict:
        """
        Make a prediction using current data
        
        Args:
            news_data: DataFrame with news articles
            current_price: Current gold price data from API
            
        Returns:
            Dictionary with prediction results
        """
        if not self.models_trained:
            # Try to load existing models
            try:
                self.load_trained_models()
            except FileNotFoundError:
                raise ValueError("Models not trained. Call train_models() first.")
        
        if self.processed_data is None:
            self.process_data()
        
        # Get news sentiment if provided
        news_sentiment = None
        if news_data is not None and not news_data.empty:
            news_sentiment = self.news_fetcher.analyze_news_impact(news_data)
        
        # Get current price if not provided
        if current_price is None:
            current_price = self.gold_api.get_current_price()
        
        # Create feature matrix
        X = self.feature_engineer.create_feature_matrix(
            self.processed_data,
            news_sentiment=news_sentiment,
            current_api_price=current_price
        )
        
        # Make prediction
        prediction = self.predictor.predict(X)
        
        # Add additional context
        result = {
            **prediction,
            'timestamp': datetime.now().isoformat(),
            'current_price': current_price.get('current_price') if current_price else None,
            'news_impact': news_sentiment,
            'model_version': '1.0.0'
        }
        
        return result
    
    def get_latest_news(self, max_results: int = 20) -> pd.DataFrame:
        """Fetch latest impactful news"""
        return self.news_fetcher.get_all_relevant_gold_news(max_results_per_query=max_results)
    
    def get_current_price(self) -> Dict:
        """Get current gold price from API"""
        return self.gold_api.get_current_price()
    
    def run_full_cycle(self) -> Dict:
        """Run full prediction cycle: fetch data, train models, predict"""
        print("=" * 70)
        print("Gold Price Prediction - Full Cycle")
        print("=" * 70)
        
        # Load and process data
        self.process_data()
        
        # Train models (or load if exists)
        try:
            self.load_trained_models()
            print("Loaded existing trained models")
        except FileNotFoundError:
            print("Training new models...")
            metrics = self.train_models()
            print(f"Models trained. Accuracy: {metrics['direction']['accuracy']:.2%}")
        
        # Get latest news
        print("\nFetching latest news...")
        news = self.get_latest_news(max_results=20)
        
        # Get current price
        print("Fetching current gold price...")
        current_price = self.get_current_price()
        
        # Make prediction
        print("\nMaking prediction...")
        prediction = self.predict(news_data=news, current_price=current_price)
        
        print("\n" + "=" * 70)
        print("PREDICTION RESULTS")
        print("=" * 70)
        print(f"Direction: {prediction['direction']}")
        print(f"Confidence: {prediction['confidence']:.1f}%")
        print(f"Expected Price Change: ${prediction['price_change']:.2f}")
        print(f"Current Price: ${prediction.get('current_price', 'N/A')}")
        
        return prediction

