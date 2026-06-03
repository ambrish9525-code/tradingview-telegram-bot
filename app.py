from flask import Flask, request
import requests
import os
import threading
import time

app = Flask(*name*)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

DELETE_AFTER_SECONDS = 10  # Test with 10 seconds

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

    result = response.json()

    # Delete ONLY TEST messages
    if result.get("ok") and message.startswith("TEST"):

        message_id = result["result"]["message_id"]

        def delete_later():

            time.sleep(DELETE_AFTER_SECONDS)

            delete_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"

            requests.post(
                delete_url,
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
        "status": "success",
        "telegram_response": response.text
    }, 200

except Exception as e:

    return {
        "status": "error",
        "message": str(e)
    }, 500


if *name* == "*main*":
app.run(host="0.0.0.0", port=10000)
