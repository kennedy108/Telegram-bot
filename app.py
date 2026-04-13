import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from database import init_db, save_user, get_user
from telegram_bot import TelegramBot
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()
app = Flask(__name__)
bot = TelegramBot(os.environ.get("TELEGRAM_BOT_TOKEN"))
init_db()
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@app.route("/webhook", methods = ["POST"])
def webhook():
    expected_secret = os.environ.get("WEBHOOK_SECRET")
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != expected_secret:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    if not data:
        return jsonify({"error": "No data"}), 400
    try:
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        username = message.get("chat", {}).get("username")
        text = message.get("text")

        if text == "/start":
            bot.register_user(chat_id, username)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": "Something went wrong"}), 500

@app.route("/notify/<username>", methods=["POST"])
@limiter.limit("5 per minute")
def notify_user(username):
    if not username or len(username) > 32:
        return jsonify({"error": "Invalid username"}), 400

    message = request.json.get("message", "You have a new notification!")
    chat_id = get_user(username)

    if chat_id is None:
        return jsonify({"error": "User not found"}), 404

    bot.send_notification(chat_id, message)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)),
            debug=os.environ.get("FLASK_DEBUG", "False") == "True")
