#!/usr/bin/env python3
"""
Gold Price Prediction Application - Main Entry Point

Run the full application with all features:
- Data loading and processing
- Model training
- Real-time predictions
- Live dashboard
"""

import sys
import argparse
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core import GoldPriceApp
from app.config import Config


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Gold Price Prediction Application')
    parser.add_argument(
        '--mode',
        choices=['train', 'predict', 'dashboard', 'full'],
        default='full',
        help='Operation mode: train models, make prediction, run dashboard, or full cycle'
    )
    parser.add_argument(
        '--load-models',
        action='store_true',
        help='Load existing trained models instead of training new ones'
    )
    
    args = parser.parse_args()
    
    # Initialize app
    app = GoldPriceApp()
    
    print("=" * 70)
    print("Gold Price Prediction Application")
    print("=" * 70)
    print(f"Mode: {args.mode}")
    print("")
    
    if args.mode == 'train':
        # Train models only
        print("Training models...")
        app.load_historical_data()
        app.process_data()
        metrics = app.train_models()
        print(f"\nTraining complete!")
        print(f"Direction Model Accuracy: {metrics['direction']['accuracy']:.2%}")
        print(f"Range Model MAE: ${metrics['range']['mae']:.2f}")
        print(f"Range Model RMSE: ${metrics['range']['rmse']:.2f}")
    
    elif args.mode == 'predict':
        # Make prediction only
        if args.load_models:
            app.load_trained_models()
        else:
            app.train_models()
        
        prediction = app.run_full_cycle()
        return prediction
    
    elif args.mode == 'dashboard':
        # Run dashboard
        print("Starting dashboard...")
        print("The dashboard will open in your browser.")
        print("Press Ctrl+C to stop.\n")
        
        import subprocess
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "live_dashboard.py",
            "--server.port", "8501"
        ])
    
    elif args.mode == 'full':
        # Full cycle: train, predict, and show results
        prediction = app.run_full_cycle()
        return prediction


if __name__ == "__main__":
    try:
        result = main()
        if result:
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

