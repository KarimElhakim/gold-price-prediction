# Quick Start Guide - Live Dashboard

## Run Dashboard Locally

### Option 1: Simple Command
```bash
streamlit run live_dashboard.py
```

### Option 2: Using Helper Script
```bash
python run_dashboard.py
```

### Option 3: With Custom Port
```bash
streamlit run live_dashboard.py --server.port 8501
```

## What You'll See

1. **Real-time Gold Price** - Live updates from GoldAPI.io
2. **Price Chart** - Interactive historical price tracking
3. **Latest News** - Impactful gold-related news with sentiment analysis
4. **Model Predictions** - UP/DOWN/NEUTRAL predictions with confidence
5. **Performance Metrics** - Model accuracy and tracking stats

## Dashboard Features

### Auto-Refresh
- Enable in sidebar
- Set refresh interval (30-300 seconds)
- Automatic data updates

### News Analysis
- Bullish/Bearish indicators
- Sentiment scores
- Relevance rankings
- Categorized by impact direction

### Model Predictions
- Real-time direction predictions
- Confidence percentages
- Signal strength metrics

## Troubleshooting

**Port already in use?**
```bash
streamlit run live_dashboard.py --server.port 8502
```

**No news appearing?**
- Check internet connection
- Click "Update Now" in sidebar
- Verify Google RSS is accessible

**API errors?**
- Check API key in environment variables
- Verify rate limits (10/hour for free tier)
- Check error messages in dashboard

## Next Steps

- View `DASHBOARD_README.md` for full documentation
- Deploy to GitHub Pages using workflows
- Or deploy to Streamlit Cloud for public access

