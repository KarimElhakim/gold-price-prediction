#!/usr/bin/env python3
"""
Run the application locally with automatic setup
"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'streamlit', 
        'plotly', 'feedparser', 'textblob', 'requests', 'kagglehub', 'joblib'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed!")
    else:
        print("All dependencies are installed ✓")

def setup_directories():
    """Create necessary directories"""
    from app.config import Config
    Config.setup_directories()
    print("Directories created ✓")

def main():
    """Main function to run the application"""
    print("=" * 70)
    print("Gold Price Prediction Application - Local Setup")
    print("=" * 70)
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Setup directories
    setup_directories()
    
    print()
    print("Starting dashboard...")
    print("The dashboard will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print()
    
    # Run dashboard
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "live_dashboard.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()

