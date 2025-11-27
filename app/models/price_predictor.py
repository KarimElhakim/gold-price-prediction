"""
Gold price prediction models
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, mean_squared_error
import joblib
from pathlib import Path
from typing import Optional, Tuple, Dict

from app.config import Config


class DirectionModel:
    """Model to predict gold price direction (UP/DOWN)"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
    
    def train(self, X: np.ndarray, y: np.ndarray, feature_names: Optional[list] = None) -> Dict:
        """Train the direction prediction model"""
        # Remove NaN values
        valid_mask = ~np.isnan(y)
        X_clean = X[valid_mask]
        y_clean = y[valid_mask]
        
        if len(X_clean) == 0:
            raise ValueError("No valid data for training")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y_clean,
            test_size=Config.TEST_SIZE,
            random_state=Config.MODEL_RANDOM_STATE
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=Config.RF_CLASSIFIER_N_ESTIMATORS,
            max_depth=Config.RF_CLASSIFIER_MAX_DEPTH,
            random_state=Config.MODEL_RANDOM_STATE,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        self.feature_names = feature_names
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        metrics = {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        return metrics
    
    def predict(self, X: np.ndarray) -> Tuple[str, float]:
        """
        Predict price direction
        Returns: (direction, confidence)
        """
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]
        proba = self.model.predict_proba(X_scaled)[0]
        
        direction = "UP" if prediction == 1 else "DOWN"
        confidence = float(max(proba)) * 100
        
        return direction, confidence
    
    def save(self, filepath: Path):
        """Save model to file"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, filepath)
    
    def load(self, filepath: Path):
        """Load model from file"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data.get('feature_names')


class RangeModel:
    """Model to predict gold price range (amount of change)"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
    
    def train(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Train the price range prediction model"""
        # Remove NaN values
        valid_mask = ~np.isnan(y)
        X_clean = X[valid_mask]
        y_clean = y[valid_mask]
        
        if len(X_clean) == 0:
            raise ValueError("No valid data for training")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y_clean,
            test_size=Config.TEST_SIZE,
            random_state=Config.MODEL_RANDOM_STATE
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=Config.RF_REGRESSOR_N_ESTIMATORS,
            max_depth=Config.RF_REGRESSOR_MAX_DEPTH,
            random_state=Config.MODEL_RANDOM_STATE,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        metrics = {
            'mae': mae,
            'rmse': rmse,
            'mean_actual': float(y_test.mean()),
            'mean_predicted': float(y_pred.mean())
        }
        
        return metrics
    
    def predict(self, X: np.ndarray) -> float:
        """Predict price change amount"""
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]
        return float(prediction)
    
    def save(self, filepath: Path):
        """Save model to file"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler
        }
        joblib.dump(model_data, filepath)
    
    def load(self, filepath: Path):
        """Load model from file"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']


class PricePredictor:
    """Main predictor class combining direction and range models"""
    
    def __init__(self):
        self.direction_model = DirectionModel()
        self.range_model = RangeModel()
    
    def train(self, X: np.ndarray, y_direction: np.ndarray, y_range: np.ndarray,
              feature_names: Optional[list] = None) -> Dict:
        """Train both models"""
        print("Training direction model...")
        direction_metrics = self.direction_model.train(X, y_direction, feature_names)
        
        print("Training range model...")
        range_metrics = self.range_model.train(X, y_range)
        
        return {
            'direction': direction_metrics,
            'range': range_metrics
        }
    
    def predict(self, X: np.ndarray) -> Dict:
        """Make predictions with both models"""
        direction, confidence = self.direction_model.predict(X)
        price_change = self.range_model.predict(X)
        
        return {
            'direction': direction,
            'confidence': confidence,
            'price_change': price_change
        }
    
    def save_models(self, models_dir: Path):
        """Save both models"""
        models_dir.mkdir(exist_ok=True)
        self.direction_model.save(models_dir / "direction_model.pkl")
        self.range_model.save(models_dir / "range_model.pkl")
    
    def load_models(self, models_dir: Path):
        """Load both models"""
        self.direction_model.load(models_dir / "direction_model.pkl")
        self.range_model.load(models_dir / "range_model.pkl")

