"""
Test script to verify all dependencies are installed and working correctly.
This simulates the key functionality of the notebook.
"""

import sys
import traceback

def test_imports():
    """Test all required imports"""
    print("=" * 60)
    print("Testing Package Imports")
    print("=" * 60)
    
    packages = {
        'pandas': 'pd',
        'numpy': 'np',
        'sklearn': 'sklearn',
        'matplotlib.pyplot': 'plt',
        'seaborn': 'sns',
        'feedparser': 'feedparser',
        'requests': 'requests',
        'bs4': 'BeautifulSoup',
        'textblob': 'TextBlob',
        'kagglehub': 'kagglehub',
    }
    
    failed = []
    for module, alias in packages.items():
        try:
            __import__(module)
            print(f"✓ {module:20s} - OK")
        except ImportError as e:
            print(f"✗ {module:20s} - FAILED: {e}")
            failed.append(module)
    
    return len(failed) == 0, failed

def test_sklearn_functionality():
    """Test scikit-learn basic functionality"""
    print("\n" + "=" * 60)
    print("Testing scikit-learn Functionality")
    print("=" * 60)
    
    try:
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        # Create dummy data
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 2, 100)
        
        # Test train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        print(f"✓ train_test_split - OK (Train: {len(X_train)}, Test: {len(X_test)})")
        
        # Test Random Forest
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print(f"✓ RandomForestClassifier - OK (Test Score: {score:.3f})")
        
        return True
    except Exception as e:
        print(f"✗ scikit-learn test failed: {e}")
        traceback.print_exc()
        return False

def test_textblob_functionality():
    """Test TextBlob sentiment analysis"""
    print("\n" + "=" * 60)
    print("Testing TextBlob Functionality")
    print("=" * 60)
    
    try:
        from textblob import TextBlob
        
        # Test sentiment analysis
        test_text = "Gold prices surge to new highs as demand increases"
        blob = TextBlob(test_text)
        sentiment = blob.sentiment.polarity
        
        print(f"✓ TextBlob import - OK")
        print(f"  Test text: '{test_text}'")
        print(f"  Sentiment score: {sentiment:.3f}")
        
        return True
    except Exception as e:
        print(f"✗ TextBlob test failed: {e}")
        traceback.print_exc()
        return False

def test_feedparser_functionality():
    """Test feedparser RSS parsing"""
    print("\n" + "=" * 60)
    print("Testing Feedparser Functionality")
    print("=" * 60)
    
    try:
        import feedparser
        
        # Test parsing (use a simple RSS feed)
        test_url = "https://news.google.com/rss/search?q=gold&hl=en-US&gl=US&ceid=US:en"
        print(f"  Testing RSS feed parsing...")
        
        # Just test import and basic structure, don't actually fetch (may be slow)
        print(f"✓ feedparser import - OK")
        print(f"  (Skipping live RSS fetch for speed)")
        
        return True
    except Exception as e:
        print(f"✗ feedparser test failed: {e}")
        return False

def test_requests_functionality():
    """Test requests library"""
    print("\n" + "=" * 60)
    print("Testing Requests Functionality")
    print("=" * 60)
    
    try:
        import requests
        
        # Test simple request
        response = requests.get("https://httpbin.org/get", timeout=5)
        print(f"✓ requests library - OK (Status: {response.status_code})")
        
        return True
    except Exception as e:
        print(f"✗ requests test failed: {e}")
        return False

def test_pandas_functionality():
    """Test pandas basic operations"""
    print("\n" + "=" * 60)
    print("Testing Pandas Functionality")
    print("=" * 60)
    
    try:
        import pandas as pd
        import numpy as np
        
        # Create sample DataFrame
        df = pd.DataFrame({
            'price': np.random.rand(100) * 2000 + 1500,
            'date': pd.date_range('2024-01-01', periods=100)
        })
        
        # Test operations used in notebook
        df['price_change'] = df['price'].diff()
        df['ma_7'] = df['price'].rolling(window=7).mean()
        df_clean = df.bfill().ffill().dropna()
        
        print(f"✓ pandas DataFrame operations - OK")
        print(f"  Created DataFrame: {df.shape}")
        print(f"  After cleaning: {df_clean.shape}")
        print(f"  Price stats: Mean=${df['price'].mean():.2f}, Std=${df['price'].std():.2f}")
        
        return True
    except Exception as e:
        print(f"✗ pandas test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Gold Price Prediction - Dependency Test Suite")
    print("=" * 60)
    print(f"Python Version: {sys.version}")
    print("")
    
    results = []
    
    # Test imports
    imports_ok, failed_imports = test_imports()
    results.append(("Package Imports", imports_ok))
    
    if not imports_ok:
        print(f"\n❌ Missing packages: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Test functionality
    results.append(("scikit-learn Functionality", test_sklearn_functionality()))
    results.append(("TextBlob Functionality", test_textblob_functionality()))
    results.append(("Feedparser Functionality", test_feedparser_functionality()))
    results.append(("Requests Functionality", test_requests_functionality()))
    results.append(("Pandas Functionality", test_pandas_functionality()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Ready to run notebook!")
    else:
        print("❌ SOME TESTS FAILED - Please check errors above")
    print("=" * 60)

if __name__ == "__main__":
    main()

