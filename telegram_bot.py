import os, requests
from database import save_user, get_user

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# TELEGRAM BOT MODULE
# Handles sending notifications and
# registering users via Telegram Bot API


# A class to interact with the Telegram Bot API.
# Handles sending messages and registering users.
class TelegramBot:

    #Initializes the TelegramBot with a bot token.

    #@param bot_token the api for the telegram bot
    def __init__(self, bot_token):
        self.bot_token = bot_token

    #Send notification to then user based on unqiue chat id

    #@param chat_id the id of the user
    #@param message the message that is to be sent
    def send_notification(self, chat_id, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id" : chat_id,
            "text" : message
        }
        requests.post(url, json = payload)

    #Register the user to the database and sends them a welcome message

    #@param chat_id the id of the user
    #@param username the telegram username
    def register_user(self, chat_id, username):
        save_user(chat_id, username)
        self.send_notification(chat_id, "Hello")