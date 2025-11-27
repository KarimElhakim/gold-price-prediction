# Streamlit Cloud Deployment Guide

## Quick Deploy

1. **Go to Streamlit Cloud**: https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Fill in**:
   - Repository: `KarimElhakim/gold-price-prediction`
   - Branch: `main`
   - Main file: `live_dashboard.py`
5. **Click "Deploy!"**

## Environment Variables (Required)

Set these in Streamlit Cloud (App settings → Secrets):

```
KAGGLE_API_TOKEN=your-kaggle-token
GOLDAPI_API_KEY=your-goldapi-key
```

Or create `.streamlit/secrets.toml` file:

```toml
KAGGLE_API_TOKEN = "your-kaggle-token"
GOLDAPI_API_KEY = "your-goldapi-key"
```

## Auto-Deploy Setup

The app will automatically redeploy when you push to `main` branch.

## Troubleshooting

### Import Errors
- Ensure `live_dashboard.py` is set as the main file
- Check that all files are committed to GitHub

### Missing Dependencies
- All dependencies are in `requirements.txt`
- Streamlit Cloud will install them automatically

### API Errors
- Verify secrets are set correctly
- Check API keys are valid

## App URL

After deployment, your app will be at:
`https://gold-price-prediction-karimelhakim.streamlit.app/`

