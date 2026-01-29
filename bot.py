import requests
import os

# These are the keys you hid in the Settings
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def get_halts():
    url = "https://www.nyse.com/api/trade-halts/current"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    return r.json().get('results', [])

# Checking for halts
halts = get_halts()
if halts:
    for row in halts:
        symbol = row.get('symbol')
        reason = row.get('reason')
        time_halt = row.get('haltTime')
        # We send an alert for EVERY halt to be 100% safe
        send_telegram(f"🚨 <b>NEW HALT: {symbol}</b>\nTime: {time_halt}\nReason: {reason}")
else:
    print("No halts found.")
