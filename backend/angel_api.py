from SmartApi.smartConnect import SmartConnect
import pyotp
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_pin = os.getenv("CLIENT_PIN")
api_key = os.getenv("API_KEY")
totp_key = os.getenv("TOTP_KEY")

def angel_login():
    try:
        obj = SmartConnect(api_key=api_key)
        totp = pyotp.TOTP(totp_key).now()
        session = obj.generateSession(client_id, client_pin, totp)
        feed_token = obj.getfeedToken()
        return obj, feed_token
    except Exception as e:
        print("[❌] Login failed:", str(e))
        return None, None
