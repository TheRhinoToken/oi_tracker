import requests
from datetime import datetime, timedelta

def get_nifty_spot_price():
    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        spot = data['records']['underlyingValue']
        return round(spot, 2)
    except Exception as e:
        print("[❌] CMP fetch error:", e)
        return None

def get_nearest_expiry():
    today = datetime.now().date()
    weekday = today.weekday()  # Monday=0, Thursday=3
    days_ahead = (3 - weekday) % 7
    expiry = today + timedelta(days=days_ahead)
    return expiry.strftime("%d-%b-%Y").upper()  # e.g., 11-JUL-2025

def get_option_chain_data():
    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return data["records"]["data"]  # This is a list of strike-wise data
    except Exception as e:
        print("[❌] Option chain fetch error:", e)
        return []

