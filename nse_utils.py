from datetime import datetime, timedelta
import requests

def get_nifty_spot_price():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        spot = data['records']['underlyingValue']
        return round(spot, 2)
    except Exception as e:
        print("[❌] Error fetching Nifty CMP:", str(e))
        return None

def get_nearest_expiry():
    today = datetime.now().date()
    weekday = today.weekday()
    days_ahead = (3 - weekday) % 7  # Thursday = 3
    expiry = today + timedelta(days=days_ahead)
    return expiry.strftime("%d-%b-%Y").upper()  # Format: 11-JUL-2024
