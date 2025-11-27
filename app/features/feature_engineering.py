"""
Feature engineering for gold price prediction
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict
from datetime import datetime


class FeatureEngineer:
    """Engineer features from historical data, news, and API data"""
    
    def __init__(self):
        pass
    
    def create_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features from historical price data"""
        df = df.copy()
        
        # Ensure date column is datetime
        date_col = None
        for col in ['Date', 'date', 'DATE', 'Date/Time']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.sort_values(date_col).reset_index(drop=True)
        
        # Price columns (handle various naming conventions)
        price_col = None
        for col in ['Price', 'price', 'PRICE', 'Close', 'close', 'CLOSE', 'USD']:
            if col in df.columns:
                price_col = col
                break
        
        if price_col is None:
            # Try to find numeric columns that might be price
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                price_col = numeric_cols[0]  # Use first numeric column
        
        if price_col is None:
            raise ValueError("Could not identify price column in dataset")
        
        # Create features
        df['price'] = pd.to_numeric(df[price_col], errors='coerce')
        df['price_change'] = df['price'].diff()
        df['price_change_pct'] = df['price'].pct_change() * 100
        df['price_ma_7'] = df['price'].rolling(window=7).mean()
        df['price_ma_30'] = df['price'].rolling(window=30).mean()
        df['price_std_7'] = df['price'].rolling(window=7).std()
        df['volatility'] = df['price_change_pct'].rolling(window=7).std()
        
        # Price momentum
        df['momentum_7'] = df['price'] - df['price'].shift(7)
        df['momentum_30'] = df['price'] - df['price'].shift(30)
        
        # Forward fill missing values
        df = df.bfill().ffill()
        
        # Create target variables
        df['next_price'] = df['price'].shift(-1)
        df['next_price_change'] = df['next_price'] - df['price']
        df['next_direction'] = (df['next_price_change'] > 0).astype(int)
        
        return df
    
    def create_feature_matrix(
        self,
        df_processed: pd.DataFrame,
        news_sentiment: Optional[Dict] = None,
        current_api_price: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Create feature matrix combining historical data, news sentiment, and API price
        """
        features = []
        
        # Historical price features
        price_features = [
            'price_change', 'price_change_pct', 'price_ma_7', 'price_ma_30',
            'price_std_7', 'volatility', 'momentum_7', 'momentum_30'
        ]
        
        # Use latest values (last row)
        if len(df_processed) > 0:
            latest = df_processed.iloc[-1]
            for feature in price_features:
                if feature in df_processed.columns:
                    val = latest[feature]
                    features.append(float(val) if not pd.isna(val) else 0.0)
                else:
                    features.append(0.0)
        else:
            # If no data, fill with zeros
            features.extend([0.0] * len(price_features))
        
        # News sentiment features
        if news_sentiment:
            features.append(float(news_sentiment.get('avg_sentiment', 0.0)))
            features.append(float(news_sentiment.get('avg_price_indicator', 0.0)))
            features.append(float(news_sentiment.get('net_signal', 0.0)))
            features.append(float(news_sentiment.get('total_news', 0)))
        else:
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # API price features
        if current_api_price and current_api_price.get('current_price'):
            features.append(float(current_api_price.get('price_change', 0.0)))
            features.append(float(current_api_price.get('price_change_pct', 0.0)))
            features.append(float(current_api_price.get('high_price', 0.0)))
            features.append(float(current_api_price.get('low_price', 0.0)))
        else:
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # Return as numpy array with proper shape
        feature_array = np.array(features).reshape(1, -1)
        
        return feature_array
    
    def get_feature_names(self) -> list:
        """Get list of feature names"""
        return [
            # Historical features (8)
            'price_change', 'price_change_pct', 'price_ma_7', 'price_ma_30',
            'price_std_7', 'volatility', 'momentum_7', 'momentum_30',
            # News features (4)
            'news_sentiment', 'news_price_indicator', 'news_net_signal', 'news_count',
            # API features (4)
            'api_price_change', 'api_price_change_pct', 'api_high', 'api_low'
        ]

