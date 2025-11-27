# Live Gold Price Prediction Dashboard

High-end, intuitive dashboard for real-time gold price monitoring, news analysis, and model performance tracking.

## Features

### 💰 Real-time Gold Price
- Live spot price updates from GoldAPI.io
- Bid/Ask prices and daily ranges
- Interactive price charts with historical data
- Price change indicators and trends

### 📰 Latest Impactful News
- Automated news fetching from Google RSS
- Intelligent filtering for gold-relevant news
- Price impact analysis (Bullish/Bearish indicators)
- Sentiment analysis per article
- News categorized by impact direction

### 🤖 Model Predictions
- Real-time price direction predictions (UP/DOWN/NEUTRAL)
- Confidence scores
- Signal strength analysis
- Performance tracking

### 📊 Performance Metrics
- Model accuracy tracking
- Prediction history
- API usage monitoring
- Update frequency tracking

## Local Setup

### Quick Start

```bash
# Install dashboard dependencies
pip install streamlit plotly

# Run the dashboard
streamlit run live_dashboard.py

# Or use the helper script
python run_dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables (optional):**
   ```bash
   export GOLDAPI_API_KEY="your-api-key-here"
   ```

3. **Run dashboard:**
   ```bash
   streamlit run live_dashboard.py
   ```

## Dashboard Controls

### Sidebar Options
- **Auto Refresh**: Enable/disable automatic data updates
- **Refresh Interval**: Set update frequency (30-300 seconds)
- **Update Now**: Manually trigger data refresh

### Main Sections
1. **Price Display**: Large, color-coded current price
2. **Price Chart**: Interactive real-time price history
3. **News Dashboard**: Latest impactful news with analysis
4. **Model Prediction**: Current prediction with confidence
5. **Performance Metrics**: Model performance tracking

## Configuration

### API Keys
- **GoldAPI.io**: Set `GOLDAPI_API_KEY` environment variable
- Default key is in the code (for testing only)

### Rate Limits
- GoldAPI.io: 10 requests/hour (free tier)
- Google RSS: No strict limits (be respectful)

## GitHub Pages Deployment

The dashboard can be deployed to GitHub Pages using GitHub Actions workflows.

### Setup GitHub Pages

1. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: GitHub Actions

2. **Add Secrets (if needed):**
   - Repository Settings → Secrets and variables → Actions
   - Add `GOLDAPI_API_KEY` secret

3. **Workflow runs automatically:**
   - On every push to main
   - Every hour (scheduled)
   - Manual trigger available

### Alternative: Streamlit Cloud

For full interactive dashboard, deploy to Streamlit Cloud:
1. Connect GitHub repository
2. Select `live_dashboard.py` as main file
3. Add environment variables
4. Deploy!

## Dashboard Features

### News Analysis
- **Bullish News**: Articles suggesting price increase
- **Bearish News**: Articles suggesting price decrease
- **Relevance Scoring**: ML-based relevance ranking
- **Sentiment Analysis**: Positive/negative sentiment per article

### Price Prediction
- Combines price trends with news sentiment
- Provides direction (UP/DOWN/NEUTRAL)
- Confidence percentage
- Signal strength metric

### Real-time Updates
- Automatic refresh at configured intervals
- Manual refresh button
- Live price tracking
- News feed updates

## Troubleshooting

### Dashboard won't start
- Check Streamlit installation: `pip install streamlit`
- Verify Python version: 3.8+
- Check port 8501 is available

### No news appearing
- Check internet connection
- Verify Google RSS is accessible
- Check rate limits

### API errors
- Verify API key is correct
- Check rate limit status
- Review error messages in dashboard

## Development

### Customization
- Modify `live_dashboard.py` for custom features
- Update refresh intervals in sidebar
- Adjust news query keywords in `fetch_latest_news()`

### Adding Features
- Model performance charts
- Historical prediction accuracy
- Export functionality
- Alerts and notifications

## Notes

- Dashboard requires active internet connection
- GoldAPI.io free tier: 10 requests/hour
- For production, consider upgrading API tiers
- Streamlit Cloud is recommended for public hosting

