import random
import requests

def get_live_price(symbol, source):
    if source == "Yahoo Finance":
        try:
            # Seedha Yahoo Finance ke hidden JSON API ko call karna
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
            # Yahoo bot-protection bypass karne ke liye headers zaroori hain
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            
            # JSON se current price nikalna
            current_price = data['chart']['result'][0]['meta']['regularMarketPrice']
            return round(current_price, 2)
            
        except Exception as e:
            return None
    else:
        # Dummy Broker API Logic
        base_prices = {"RELIANCE.NS": 2490, "TCS.NS": 3790, "HDFCBANK.NS": 1595}
        current_price = base_prices.get(symbol, 100) + random.uniform(-15, 15)
        return round(current_price, 2)
        
