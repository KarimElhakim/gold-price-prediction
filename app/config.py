"""
Configuration management for the Gold Price Prediction application
"""

import os
from pathlib import Path
from typing import Optional

class Config:
    """Application configuration"""
    
    # API Keys (can be set via environment variables or Streamlit secrets)
    try:
        import streamlit as st
        # Try to get from Streamlit secrets first
        KAGGLE_API_TOKEN: str = st.secrets.get("KAGGLE_API_TOKEN", os.getenv("KAGGLE_API_TOKEN", "KGAT_b352cb91c46b038224e3d90adb8d8c32"))
        GOLDAPI_API_KEY: str = st.secrets.get("GOLDAPI_API_KEY", os.getenv("GOLDAPI_API_KEY", "goldapi-ap54smihd5h4h-io"))
    except (ImportError, AttributeError, FileNotFoundError):
        # Fallback to environment variables or defaults
        KAGGLE_API_TOKEN: str = os.getenv("KAGGLE_API_TOKEN", "KGAT_b352cb91c46b038224e3d90adb8d8c32")
        GOLDAPI_API_KEY: str = os.getenv("GOLDAPI_API_KEY", "goldapi-ap54smihd5h4h-io")
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    CACHE_DIR: Path = BASE_DIR / ".cache"
    
    # GoldAPI.io settings
    GOLDAPI_BASE_URL: str = "https://www.goldapi.io/api/XAU/USD"
    GOLDAPI_RATE_LIMIT: int = 10  # requests per hour (free tier)
    
    # Model settings
    MODEL_RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.2
    
    # Random Forest settings
    RF_CLASSIFIER_N_ESTIMATORS: int = 100
    RF_CLASSIFIER_MAX_DEPTH: int = 10
    RF_REGRESSOR_N_ESTIMATORS: int = 100
    RF_REGRESSOR_MAX_DEPTH: int = 10
    
    # News settings
    NEWS_MAX_RESULTS_PER_QUERY: int = 50
    NEWS_MIN_RELEVANCE_SCORE: float = 0.5
    NEWS_QUERY_LANGUAGES: list = ["en"]
    
    # Dashboard settings
    DASHBOARD_REFRESH_INTERVAL: int = 60  # seconds
    DASHBOARD_PRICE_HISTORY_SIZE: int = 100
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.MODELS_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)
        
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate that required API keys are set"""
        validation = {
            "kaggle": bool(cls.KAGGLE_API_TOKEN),
            "goldapi": bool(cls.GOLDAPI_API_KEY)
        }
        return validation

# Set up directories on import
Config.setup_directories()

# Set Kaggle environment variable
os.environ['KAGGLE_API_TOKEN'] = Config.KAGGLE_API_TOKEN

