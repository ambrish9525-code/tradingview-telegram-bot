from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/")
def home():
    return "Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        data = request.json

        message = data.get("message", str(data))

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(
            telegram_url,
            json=payload,
            timeout=10
        )

        return {
            "status": "success",
            "telegram_response": response.text
        }, 200

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
