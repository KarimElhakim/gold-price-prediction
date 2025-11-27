"""
Setup script for Gold Price Prediction Application
Ensures all dependencies and structure are correct
"""

from setuptools import setup, find_packages

setup(
    name="gold-price-prediction",
    version="1.0.0",
    description="Gold Price Prediction Application with ML models and real-time data",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "feedparser>=6.0.10",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "textblob>=0.17.1",
        "kagglehub>=0.2.0",
        "joblib>=1.3.0",
    ],
    python_requires=">=3.8",
)

