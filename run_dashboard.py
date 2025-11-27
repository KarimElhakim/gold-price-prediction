"""
Simple script to run the dashboard locally
Usage: python run_dashboard.py
"""

import subprocess
import sys
import os

def main():
    print("="*70)
    print("Starting Gold Price Prediction Dashboard...")
    print("="*70)
    print("\nDashboard will open in your default browser")
    print("Press Ctrl+C to stop the dashboard\n")
    
    # Set environment variables
    os.environ['GOLDAPI_API_KEY'] = os.getenv('GOLDAPI_API_KEY', 'goldapi-ap54smihd5h4h-io')
    
    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            "live_dashboard.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\nDashboard stopped by user")
    except Exception as e:
        print(f"\nError starting dashboard: {e}")
        print("\nMake sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()

