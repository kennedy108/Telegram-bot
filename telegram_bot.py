import os, requests
from database import save_user, get_user

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

class TelegramBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token

    def send_notification(self, chat_id, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id" : chat_id,
            "text" : message
        }
        requests.post(url, json = payload)

    def register_user(self, chat_id, username):
        save_user(chat_id, username)
        self.send_notification(chat_id, "Hello")