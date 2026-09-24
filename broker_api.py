import random
import yfinance as yf

def get_live_price(symbol, source):
    if source == "Yahoo Finance":
        try:
            # Yahoo finance se live data fetch karna
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                return round(current_price, 2)
            return None
        except Exception:
            return None
    else:
        # Dummy/Custom Broker API Logic (Ise aap baad mein apne real API se badal sakte hain)
        base_prices = {"RELIANCE.NS": 2490, "TCS.NS": 3790, "HDFCBANK.NS": 1595}
        current_price = base_prices.get(symbol, 100) + random.uniform(-15, 15)
        return round(current_price, 2)
        
