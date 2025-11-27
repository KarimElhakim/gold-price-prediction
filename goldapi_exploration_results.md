# GoldAPI.io API Exploration Results

## ✅ Working Endpoint

**Primary Endpoint**: `XAU/USD`
- **Base URL**: `https://www.goldapi.io/api/XAU/USD`
- **Method**: GET
- **Authentication**: Header `x-access-token: {API_KEY}`
- **Status**: ✅ Working perfectly

## API Response Structure

```json
{
  "timestamp": 1764243835,
  "metal": "XAU",
  "currency": "USD",
  "exchange": "FOREXCOM",
  "symbol": "FOREXCOM:XAUUSD",
  "prev_close_price": 4163.815,
  "open_price": 4163.815,
  "low_price": 4142.71,
  "high_price": 4168.815,
  "open_time": 1764201600,
  "price": 4161.39,              // Current spot price per ounce
  "ch": -2.42,                   // Price change (absolute)
  "chp": -0.05,                  // Price change percentage
  "ask": 4161.75,                // Ask price
  "bid": 4161.12,                // Bid price
  "price_gram_24k": 133.7918,    // Price per gram (24k)
  "price_gram_22k": 122.6425,
  "price_gram_21k": 117.0678,
  "price_gram_20k": 111.4932,
  "price_gram_18k": 100.3438,
  "price_gram_16k": 89.1945,
  "price_gram_14k": 78.0452,
  "price_gram_10k": 55.7466
}
```

## Rate Limits

- **Free Tier**: 10 requests per hour
- **Rate Limit Header**: `X-Ratelimit-Limit: 10`
- **Remaining**: `X-Ratelimit-Remaining: 9`
- **Reset**: `X-Ratelimit-Reset: {timestamp}` (hourly reset)

## Key Features

1. **Real-time Data**: Current spot price updated frequently
2. **Comprehensive Pricing**: Price per ounce, bid/ask, multiple gram prices
3. **Price Changes**: Absolute change (ch) and percentage change (chp)
4. **Market Data**: High, low, open, previous close
5. **Exchange Info**: FOREXCOM exchange data
6. **Timestamps**: Unix timestamps for price and open time

## Best Practices

- Use `price` field for current gold price per ounce (primary use case)
- `ch` and `chp` for price movement analysis
- `bid` and `ask` for trading spread information
- `high_price` and `low_price` for daily range analysis
- Monitor rate limits (10/hour on free tier)

## Integration

Perfect for our model because:
- ✅ Direct gold price (no conversion needed)
- ✅ Real-time/live data
- ✅ Multiple price metrics for feature engineering
- ✅ Price change data for trend analysis
- ✅ Reliable and consistent API

