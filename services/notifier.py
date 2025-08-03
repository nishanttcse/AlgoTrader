import requests

# Optional: use your own bot token and chat ID for alerts
TELEGRAM_BOT_TOKEN = "8288236046:AAH1k5jq7Tkm8_q7ElKP38jSZupSCocb_c0"
TELEGRAM_CHAT_ID = "7992237117"

def send_alert(message):
    print(message)  # For local testing
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            requests.post(url, data=payload)
        except Exception as e:
            print(f"❌ Failed to send Telegram alert: {e}")
