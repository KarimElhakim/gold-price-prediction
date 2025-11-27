"""
Live Gold Price Prediction Dashboard - Production Version
High-end, intuitive dashboard with real-time updates, news analysis, and model performance tracking
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import requests
import feedparser
from urllib.parse import quote_plus
from textblob import TextBlob
import os
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="Gold Price Prediction Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .price-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .price-up {
        color: #00FF00;
        background: linear-gradient(135deg, #004400, #006600);
    }
    .price-down {
        color: #FF4444;
        background: linear-gradient(135deg, #440000, #660000);
    }
    .metric-card {
        background: linear-gradient(135deg, #1E1E1E, #2E2E2E);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .news-card {
        background: linear-gradient(135deg, #1E1E1E, #2E2E2E);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #FFD700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: translateX(5px);
    }
    .stAlert {
        border-radius: 10px;
    }
    .prediction-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem;
    }
    .badge-bullish {
        background: linear-gradient(135deg, #00AA00, #00FF00);
        color: white;
    }
    .badge-bearish {
        background: linear-gradient(135deg, #AA0000, #FF0000);
        color: white;
    }
    .badge-neutral {
        background: linear-gradient(135deg, #666666, #999999);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
GOLDAPI_API_KEY = os.getenv("GOLDAPI_API_KEY", "goldapi-ap54smihd5h4h-io")

# Initialize session state for data persistence
if 'gold_price_history' not in st.session_state:
    st.session_state.gold_price_history = []
if 'model_predictions' not in st.session_state:
    st.session_state.model_predictions = []
if 'news_feed' not in st.session_state:
    st.session_state.news_feed = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'performance_metrics' not in st.session_state:
    st.session_state.performance_metrics = {
        'accuracy': 0.0,
        'predictions_count': 0,
        'correct_predictions': 0
    }

def get_gold_price():
    """Fetch current gold price from GoldAPI.io"""
    BASE_URL = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        'x-access-token': GOLDAPI_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'price': float(data.get('price', 0)),
                'bid': float(data.get('bid', 0)),
                'ask': float(data.get('ask', 0)),
                'change': float(data.get('ch', 0)),
                'change_pct': float(data.get('chp', 0)),
                'high': float(data.get('high_price', 0)),
                'low': float(data.get('low_price', 0)),
                'open': float(data.get('open_price', 0)),
                'prev_close': float(data.get('prev_close_price', 0)),
                'timestamp': datetime.now(),
                'timestamp_unix': data.get('timestamp', int(time.time())),
                'rate_limit_remaining': int(response.headers.get('X-Ratelimit-Remaining', 0))
            }
    except Exception as e:
        return None

def analyze_gold_price_indicators(text):
    """Analyze text for keywords indicating price rise or fall"""
    text_lower = str(text).lower()
    
    rise_keywords = [
        'rise', 'surge', 'spike', 'rally', 'gain', 'jump', 'climb', 'increase',
        'soar', 'peak', 'high', 'bullish', 'strong', 'upward', 'momentum',
        'demand', 'safe haven', 'inflation hedge', 'uncertainty', 'crisis',
        'geopolitical', 'war', 'conflict', 'sanctions', 'trade war',
        'political instability', 'recession', 'economic downturn'
    ]
    
    fall_keywords = [
        'fall', 'drop', 'decline', 'plunge', 'crash', 'slide', 'tumble', 'dip',
        'retreat', 'low', 'bearish', 'weak', 'downward', 'lose', 'sell-off',
        'dollar strong', 'interest rate hike', 'strengthening economy',
        'risk-on', 'stock market rally', 'safe haven demand fades'
    ]
    
    rise_count = sum(1 for keyword in rise_keywords if keyword in text_lower)
    fall_count = sum(1 for keyword in fall_keywords if keyword in text_lower)
    
    if rise_count > fall_count:
        return 1
    elif fall_count > rise_count:
        return -1
    else:
        return 0

def fetch_latest_news(max_results=20):
    """Fetch latest impactful gold-related news"""
    queries = [
        "gold price OR gold market OR gold trading",
        "inflation OR interest rate OR federal reserve OR central bank",
        "geopolitical OR war OR conflict OR sanctions",
        "political instability OR election OR government policy",
        "economic crisis OR recession OR market crash"
    ]
    
    all_news = []
    
    for query in queries[:3]:  # Use first 3 queries
        try:
            encoded_query = quote_plus(query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:max_results//3]:
                title = entry.get('title', '').replace('<b>', '').replace('</b>', '')
                summary = entry.get('summary', '').replace('<b>', '').replace('</b>', '')
                full_text = f"{title} {summary}"
                
                # Analyze sentiment and impact
                blob = TextBlob(full_text)
                sentiment = blob.sentiment.polarity
                price_indicator = analyze_gold_price_indicators(full_text)
                
                # Calculate relevance score
                relevance = abs(sentiment) * 0.3 + abs(price_indicator) * 0.7
                
                all_news.append({
                    'title': title,
                    'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                    'published': entry.get('published', ''),
                    'link': entry.get('link', ''),
                    'sentiment': sentiment,
                    'price_indicator': price_indicator,
                    'relevance_score': relevance,
                    'full_text': full_text
                })
            time.sleep(0.3)  # Rate limit protection
        except Exception as e:
            continue
    
    if all_news:
        news_df = pd.DataFrame(all_news)
        news_df = news_df.sort_values('relevance_score', ascending=False).head(max_results)
        return news_df
    
    return pd.DataFrame()

def calculate_model_prediction(current_price_data, news_data):
    """Calculate model prediction based on current price and news"""
    if not current_price_data:
        return None
    
    # Simple prediction logic (can be enhanced with actual ML model)
    price_change_pct = current_price_data['change_pct']
    price_indicator = 0
    sentiment_score = 0
    
    if not news_data.empty:
        price_indicator = news_data['price_indicator'].mean()
        sentiment_score = news_data['sentiment'].mean()
    
    # Combined signal
    combined_signal = (price_change_pct * 0.4) + (price_indicator * 50 * 0.4) + (sentiment_score * 50 * 0.2)
    
    if combined_signal > 2:
        direction = "UP"
        confidence = min(95, 50 + abs(combined_signal) * 2)
    elif combined_signal < -2:
        direction = "DOWN"
        confidence = min(95, 50 + abs(combined_signal) * 2)
    else:
        direction = "NEUTRAL"
        confidence = 50
    
    return {
        'direction': direction,
        'confidence': confidence,
        'signal_strength': combined_signal,
        'timestamp': datetime.now()
    }

# Main Dashboard
def main():
    # Header
    st.markdown('<div class="main-header">💰 Gold Price Prediction Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Dashboard Controls")
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True, help="Automatically refresh data")
        refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, 60)
        
        if st.button("🔄 Update Now", use_container_width=True, type="primary"):
            with st.spinner("Updating..."):
                price_data = get_gold_price()
                if price_data:
                    st.session_state.gold_price_history.append({
                        'timestamp': price_data['timestamp'],
                        'price': price_data['price'],
                        'change': price_data['change'],
                        'change_pct': price_data['change_pct']
                    })
                    if len(st.session_state.gold_price_history) > 100:
                        st.session_state.gold_price_history = st.session_state.gold_price_history[-100:]
                    
                    st.session_state.last_update = datetime.now()
                    st.success("✅ Data updated!")
        
        st.divider()
        st.header("📊 Model Status")
        st.info(f"🟢 Active\nLast Update: {st.session_state.last_update.strftime('%H:%M:%S') if st.session_state.last_update else 'Never'}")
        
        st.divider()
        st.header("ℹ️ About")
        st.markdown("""
        **Live Dashboard Features:**
        - ⏱️ Real-time gold price updates
        - 📰 Latest impactful news
        - 🔍 Price impact analysis
        - 🤖 Model predictions
        - 📈 Performance tracking
        """)
    
    # Auto-refresh
    if auto_refresh:
        if st.session_state.last_update:
            time_since_update = (datetime.now() - st.session_state.last_update).total_seconds()
            if time_since_update >= refresh_interval:
                price_data = get_gold_price()
                if price_data:
                    st.session_state.gold_price_history.append({
                        'timestamp': price_data['timestamp'],
                        'price': price_data['price'],
                        'change': price_data['change'],
                        'change_pct': price_data['change_pct']
                    })
                    if len(st.session_state.gold_price_history) > 100:
                        st.session_state.gold_price_history = st.session_state.gold_price_history[-100:]
                    
                    st.session_state.last_update = datetime.now()
    
    # Current Gold Price Section
    price_data = get_gold_price()
    
    if price_data:
        # Price display with color coding
        price_class = "price-up" if price_data['change'] >= 0 else "price-down"
        change_symbol = "📈" if price_data['change'] >= 0 else "📉"
        
        st.markdown(f"""
        <div class="price-display {price_class}">
            {change_symbol} ${price_data['price']:,.2f}/oz
            <div style="font-size: 1.5rem; margin-top: 0.5rem;">
                {price_data['change']:+.2f} ({price_data['change_pct']:+.2f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Bid", f"${price_data['bid']:,.2f}")
        with col2:
            st.metric("Ask", f"${price_data['ask']:,.2f}")
        with col3:
            price_range = price_data['high'] - price_data['low']
            st.metric("Daily Range", f"${price_range:,.2f}")
        with col4:
            st.metric("High", f"${price_data['high']:,.2f}")
        with col5:
            st.metric("Low", f"${price_data['low']:,.2f}")
        
        # Price chart
        if st.session_state.gold_price_history:
            price_df = pd.DataFrame(st.session_state.gold_price_history)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=price_df['timestamp'],
                y=price_df['price'],
                mode='lines+markers',
                name='Gold Price',
                line=dict(color='#FFD700', width=3),
                marker=dict(size=6)
            ))
            
            # Add change indicators
            for i, row in price_df.iterrows():
                color = 'green' if row['change'] >= 0 else 'red'
                fig.add_trace(go.Scatter(
                    x=[row['timestamp']],
                    y=[row['price']],
                    mode='markers',
                    marker=dict(color=color, size=10, symbol='arrow-up' if row['change'] >= 0 else 'arrow-down'),
                    showlegend=False,
                    hovertext=f"Change: {row['change']:+.2f} ({row['change_pct']:+.2f}%)"
                ))
            
            fig.update_layout(
                title="Real-time Gold Price Chart",
                xaxis_title="Time",
                yaxis_title="Price (USD/oz)",
                height=450,
                template="plotly_dark",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # News Section
    st.header("📰 Latest Impactful News & Price Analysis")
    
    news_df = fetch_latest_news(max_results=20)
    
    if not news_df.empty:
        # News impact analysis
        rise_news = news_df[news_df['price_indicator'] > 0]
        fall_news = news_df[news_df['price_indicator'] < 0]
        neutral_news = news_df[news_df['price_indicator'] == 0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📰 Total News", len(news_df))
        with col2:
            st.metric("📈 Bullish", len(rise_news), delta=f"{len(rise_news)/len(news_df)*100:.1f}%")
        with col3:
            st.metric("📉 Bearish", len(fall_news), delta=f"{len(fall_news)/len(news_df)*100:.1f}%")
        with col4:
            avg_relevance = news_df['relevance_score'].mean()
            st.metric("⭐ Avg Relevance", f"{avg_relevance:.2f}")
        
        # Overall news signal
        net_signal = len(rise_news) - len(fall_news)
        signal_strength = abs(net_signal) / len(news_df) * 100
        
        if net_signal > 3:
            signal_badge = '<span class="prediction-badge badge-bullish">🔼 STRONG BULLISH SIGNAL</span>'
        elif net_signal > 0:
            signal_badge = '<span class="prediction-badge badge-bullish">📈 MILD BULLISH</span>'
        elif net_signal < -3:
            signal_badge = '<span class="prediction-badge badge-bearish">🔽 STRONG BEARISH SIGNAL</span>'
        elif net_signal < 0:
            signal_badge = '<span class="prediction-badge badge-bearish">📉 MILD BEARISH</span>'
        else:
            signal_badge = '<span class="prediction-badge badge-neutral">➡️ NEUTRAL</span>'
        
        st.markdown(f"**Overall News Signal:** {signal_badge} (Strength: {signal_strength:.1f}%)", unsafe_allow_html=True)
        st.markdown("---")
        
        # Display news with tabs
        tab1, tab2, tab3 = st.tabs(["🔥 Most Impactful", "📈 Bullish News", "📉 Bearish News"])
        
        with tab1:
            st.subheader("Top Impactful News (Sorted by Relevance)")
            for idx, news in news_df.head(10).iterrows():
                indicator_icon = "📈" if news['price_indicator'] > 0 else "📉" if news['price_indicator'] < 0 else "➡️"
                sentiment_emoji = "😊" if news['sentiment'] > 0.1 else "😟" if news['sentiment'] < -0.1 else "😐"
                
                with st.expander(f"{indicator_icon} {news['title'][:100]}...", expanded=False):
                    st.markdown(f"**{news['title']}**")
                    st.markdown(f"{news['summary']}")
                    st.markdown(f"**Analysis:**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Price Indicator", "RISE" if news['price_indicator'] > 0 else "FALL" if news['price_indicator'] < 0 else "NEUTRAL")
                    with col2:
                        st.metric("Sentiment", f"{sentiment_emoji} {news['sentiment']:.2f}")
                    with col3:
                        st.metric("Relevance", f"{news['relevance_score']:.2f}")
                    st.markdown(f"📅 Published: {news['published']}")
                    st.markdown(f"🔗 [Read Full Article]({news['link']})")
        
        with tab2:
            if not rise_news.empty:
                st.subheader(f"News Suggesting Price Increase ({len(rise_news)} articles)")
                for idx, news in rise_news.head(10).iterrows():
                    with st.expander(f"📈 {news['title'][:100]}...", expanded=False):
                        st.markdown(f"**{news['title']}**")
                        st.markdown(f"{news['summary']}")
                        st.markdown(f"📅 {news['published']} | 🔗 [Read More]({news['link']})")
            else:
                st.info("No bullish news found")
        
        with tab3:
            if not fall_news.empty:
                st.subheader(f"News Suggesting Price Decrease ({len(fall_news)} articles)")
                for idx, news in fall_news.head(10).iterrows():
                    with st.expander(f"📉 {news['title'][:100]}...", expanded=False):
                        st.markdown(f"**{news['title']}**")
                        st.markdown(f"{news['summary']}")
                        st.markdown(f"📅 {news['published']} | 🔗 [Read More]({news['link']})")
            else:
                st.info("No bearish news found")
    else:
        st.warning("No news available. Click 'Update Now' to fetch latest news.")
    
    # Model Prediction Section
    st.header("🤖 Model Prediction & Performance")
    
    if price_data and not news_df.empty:
        prediction = calculate_model_prediction(price_data, news_df)
        
        if prediction:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                direction_emoji = "🔼" if prediction['direction'] == "UP" else "🔽" if prediction['direction'] == "DOWN" else "➡️"
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1E1E1E, #2E2E2E); border-radius: 15px;">
                    <h2>Prediction</h2>
                    <h1 style="font-size: 4rem; margin: 1rem 0;">{direction_emoji}</h1>
                    <h2>{prediction['direction']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1E1E1E, #2E2E2E); border-radius: 15px;">
                    <h2>Confidence</h2>
                    <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction['confidence']:.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1E1E1E, #2E2E2E); border-radius: 15px;">
                    <h2>Signal Strength</h2>
                    <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction['signal_strength']:+.2f}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            # Store prediction
            st.session_state.model_predictions.append(prediction)
            if len(st.session_state.model_predictions) > 50:
                st.session_state.model_predictions = st.session_state.model_predictions[-50:]
    
    # Performance metrics
    st.subheader("📊 Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Predictions", len(st.session_state.model_predictions))
    with col2:
        st.metric("Price Updates", len(st.session_state.gold_price_history))
    with col3:
        st.metric("News Articles", len(news_df))
    with col4:
        if price_data and price_data.get('rate_limit_remaining'):
            st.metric("API Calls Remaining", f"{price_data['rate_limit_remaining']}/10")
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Last Updated:** {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.last_update else 'Never'} | **Dashboard Version:** 1.0")

if __name__ == "__main__":
    main()

