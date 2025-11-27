#!/usr/bin/env python3
"""
Run the Gold Price Prediction Application
"""

import sys
from pathlib import Path
import argparse

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gold Price Prediction Application')
    parser.add_argument(
        'command',
        choices=['train', 'predict', 'dashboard', 'full'],
        nargs='?',
        default='dashboard',
        help='Command to run'
    )
    
    args = parser.parse_args()
    
    if args.command == 'dashboard':
        import subprocess
        print("Starting dashboard...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "live_dashboard.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    else:
        from main import main
        import argparse as ap
        sys.argv = ['main.py', '--mode', args.command]
        main()

