"""
Live Gold Price Prediction Dashboard - Full Application Integration
High-end, intuitive dashboard using the full Python application framework
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

# Add app to path - ensure we can import app modules
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Import app modules
try:
    from app.core import GoldPriceApp
    from app.config import Config
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error(f"Current directory: {current_dir}")
    st.error(f"Python path: {sys.path[:3]}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Gold Price Prediction Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'app' not in st.session_state:
    st.session_state.app = GoldPriceApp()
    # Try to load models if they exist
    try:
        st.session_state.app.load_trained_models()
        st.session_state.models_loaded = True
    except FileNotFoundError:
        st.session_state.models_loaded = False

if 'gold_price_history' not in st.session_state:
    st.session_state.gold_price_history = []
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = None

def update_dashboard():
    """Update dashboard data"""
    app = st.session_state.app
    
    # Get current price
    price_data = app.get_current_price()
    if price_data and price_data.get('current_price'):
        st.session_state.gold_price_history.append({
            'timestamp': datetime.now(),
            'price': price_data['current_price'],
            'change': price_data.get('price_change', 0),
            'change_pct': price_data.get('price_change_pct', 0)
        })
        if len(st.session_state.gold_price_history) > Config.DASHBOARD_PRICE_HISTORY_SIZE:
            st.session_state.gold_price_history = st.session_state.gold_price_history[-Config.DASHBOARD_PRICE_HISTORY_SIZE:]
    
    # Get news
    news = app.get_latest_news(max_results=20)
    st.session_state.news_feed = news.to_dict('records') if not news.empty else []
    
    # Make prediction if models loaded
    if st.session_state.models_loaded:
        try:
            prediction = app.predict(news_data=news, current_price=price_data)
            st.session_state.predictions_history.append(prediction)
            if len(st.session_state.predictions_history) > 50:
                st.session_state.predictions_history = st.session_state.predictions_history[-50:]
        except Exception as e:
            st.error(f"Prediction error: {e}")
    
    st.session_state.last_update = datetime.now()

# Main Dashboard
def main():
    # Header
    st.markdown('<div class="main-header">💰 Gold Price Prediction Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controls")
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
        refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, Config.DASHBOARD_REFRESH_INTERVAL)
        
        if st.button("🔄 Update Now", use_container_width=True, type="primary"):
            with st.spinner("Updating..."):
                update_dashboard()
                st.success("✅ Data updated!")
        
        st.divider()
        st.header("📊 Model Status")
        if st.session_state.models_loaded:
            st.success("🟢 Models Loaded")
        else:
            st.warning("⚠️ Models Not Loaded")
            if st.button("Train Models", use_container_width=True):
                with st.spinner("Training models..."):
                    try:
                        st.session_state.app.process_data()
                        st.session_state.app.train_models()
                        st.session_state.models_loaded = True
                        st.success("✅ Models trained successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Training failed: {e}")
        
        st.divider()
        st.header("ℹ️ About")
        st.markdown("""
        **Live Dashboard Features:**
        - ⏱️ Real-time gold price
        - 📰 Latest impactful news
        - 🤖 ML predictions
        - 📈 Performance tracking
        """)
    
    # Auto-refresh
    if auto_refresh and st.session_state.last_update:
        time_since_update = (datetime.now() - st.session_state.last_update).total_seconds()
        if time_since_update >= refresh_interval:
            update_dashboard()
            st.rerun()
    
    # Current Gold Price
    price_data = st.session_state.app.get_current_price()
    
    if price_data and price_data.get('current_price'):
        price_class = "price-up" if price_data.get('price_change', 0) >= 0 else "price-down"
        change_symbol = "📈" if price_data.get('price_change', 0) >= 0 else "📉"
        
        st.markdown(f"""
        <div class="price-display {price_class}">
            {change_symbol} ${price_data['current_price']:,.2f}/oz
            <div style="font-size: 1.5rem; margin-top: 0.5rem;">
                {price_data.get('price_change', 0):+.2f} ({price_data.get('price_change_pct', 0):+.2f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Bid", f"${price_data.get('bid', 0):,.2f}")
        with col2:
            st.metric("Ask", f"${price_data.get('ask', 0):,.2f}")
        with col3:
            price_range = price_data.get('high_price', 0) - price_data.get('low_price', 0)
            st.metric("Daily Range", f"${price_range:,.2f}")
        with col4:
            st.metric("High", f"${price_data.get('high_price', 0):,.2f}")
        with col5:
            st.metric("Low", f"${price_data.get('low_price', 0):,.2f}")
        
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
    st.header("📰 Latest Impactful News & Analysis")
    
    news = st.session_state.app.get_latest_news(max_results=20)
    
    if not news.empty:
        rise_news = news[news['price_indicator'] > 0]
        fall_news = news[news['price_indicator'] < 0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📰 Total News", len(news))
        with col2:
            st.metric("📈 Bullish", len(rise_news), delta=f"{len(rise_news)/len(news)*100:.1f}%")
        with col3:
            st.metric("📉 Bearish", len(fall_news), delta=f"{len(fall_news)/len(news)*100:.1f}%")
        
        # Display top news
        for idx, row in news.head(10).iterrows():
            with st.expander(f"{'📈' if row['price_indicator'] > 0 else '📉' if row['price_indicator'] < 0 else '➡️'} {row['title'][:100]}...", expanded=False):
                st.markdown(f"**{row['title']}**")
                st.markdown(f"{row['summary']}")
                st.markdown(f"📅 {row['published']} | 🔗 [Read More]({row['link']})")
    else:
        st.info("No news available. Click 'Update Now' to fetch.")
    
    # Model Prediction
    st.header("🤖 Model Prediction")
    
    if st.session_state.models_loaded and st.session_state.predictions_history:
        latest_pred = st.session_state.predictions_history[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            direction_emoji = "🔼" if latest_pred['direction'] == "UP" else "🔽" if latest_pred['direction'] == "DOWN" else "➡️"
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1E1E1E, #2E2E2E); border-radius: 15px;">
                <h2>Prediction</h2>
                <h1 style="font-size: 4rem; margin: 1rem 0;">{direction_emoji}</h1>
                <h2>{latest_pred['direction']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1E1E1E, #2E2E2E); border-radius: 15px;">
                <h2>Confidence</h2>
                <h1 style="font-size: 4rem; margin: 1rem 0;">{latest_pred['confidence']:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1E1E1E, #2E2E2E); border-radius: 15px;">
                <h2>Price Change</h2>
                <h1 style="font-size: 4rem; margin: 1rem 0;">${latest_pred['price_change']:+.2f}</h1>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Models not loaded. Train models in sidebar to see predictions.")
    
    # Footer
    st.markdown("---")
    if st.session_state.last_update:
        st.markdown(f"**Last Updated:** {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
