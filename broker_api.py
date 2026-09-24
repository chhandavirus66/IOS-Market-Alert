import random

def get_live_price(symbol):
    # Yeh ek dummy API hai. Real app mein aap yahan Zerodha, Upstox ya Yahoo Finance API lagayenge.
    base_prices = {"RELIANCE": 2490, "TCS": 3790, "HDFCBANK": 1595}
    current_price = base_prices.get(symbol, 100) + random.uniform(-15, 15)
    return round(current_price, 2)
  
