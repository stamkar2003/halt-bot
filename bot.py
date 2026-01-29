import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_halts():
    url = "https://www.nyse.com/api/trade-halts/current"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        # Ensure we are looking at the right part of the data
        if isinstance(data, dict):
            return data.get('results', [])
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def send_telegram(msg):
    if not TOKEN or not CHAT_ID:
        print("Missing Telegram keys!")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

# MAIN RUN
halts = get_halts()
if halts:
    for row in halts:
        # Check if row is actually a dictionary before using .get()
        if isinstance(row, dict):
            sym = row.get('symbol', 'Unknown')
            reason = row.get('reason', 'N/A')
            tm = row.get('haltTime', 'N/A')
            send_telegram(f"🚨 <b>NEW HALT: {sym}</b>\nTime: {tm}\nReason: {reason}")
else:
    print("No active halts found right now.")
    
