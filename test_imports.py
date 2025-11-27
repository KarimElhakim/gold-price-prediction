#!/usr/bin/env python3
"""
Test all imports to ensure the application structure is correct
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports"""
    errors = []
    
    try:
        from app.config import Config
        print("✓ Config imported")
    except Exception as e:
        errors.append(f"Config: {e}")
    
    try:
        from app.data import KaggleDataFetcher, GoldAPIClient, NewsFetcher
        print("✓ Data modules imported")
    except Exception as e:
        errors.append(f"Data modules: {e}")
    
    try:
        from app.features import FeatureEngineer
        print("✓ Features imported")
    except Exception as e:
        errors.append(f"Features: {e}")
    
    try:
        from app.models import PricePredictor
        print("✓ Models imported")
    except Exception as e:
        errors.append(f"Models: {e}")
    
    try:
        from app.core import GoldPriceApp
        print("✓ Core app imported")
    except Exception as e:
        errors.append(f"Core app: {e}")
    
    try:
        app = GoldPriceApp()
        print("✓ App initialized")
    except Exception as e:
        errors.append(f"App initialization: {e}")
    
    if errors:
        print("\n✗ ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✓ All imports successful!")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

