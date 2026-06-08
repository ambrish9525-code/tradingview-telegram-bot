from flask import Flask, request
import requests
import os
import threading
import time

app = Flask(*name*)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

DELETE_AFTER_SECONDS = 10

@app.route("/")
def home():
return "Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():
try:
data = request.get_json(force=True)


    message = data.get("message", "No message")

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        telegram_url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=10
    )

    result = response.json()

    if result.get("ok") and message.startswith("TEST"):

        message_id = result["result"]["message_id"]

        def delete_later():
            time.sleep(DELETE_AFTER_SECONDS)

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                json={
                    "chat_id": CHAT_ID,
                    "message_id": message_id
                },
                timeout=10
            )

        threading.Thread(
            target=delete_later,
            daemon=True
        ).start()

    return {
        "status": "success"
    }, 200

except Exception as e:

    return {
        "status": "error",
        "message": str(e)
    }, 500


if *name* == "*main*":
app.run(host="0.0.0.0", port=10000)
