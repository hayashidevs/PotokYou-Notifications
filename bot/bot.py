import requests
import telegram
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from config import BOT_TOKEN, API_BASE_URL, load_message

# Initialize the bot with the token
bot = telegram.Bot(token=BOT_TOKEN)

def fetch_clients():
    """
    Fetch clients from the Django REST API.
    """
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()  # Return the list of clients in JSON format
    except requests.RequestException as e:
        print(f"Failed to fetch client data: {e}")
        return []

def send_message_to_clients():
    """
    Fetch clients from the API and send them a message via Telegram.
    """
    message_template = load_message()
    clients = fetch_clients()

    if not clients:
        print("No clients to send messages to.")
        return

    for client in clients:
        telegram_id = client.get('telegramid')
        username = client.get('username') or 'Client'

        # Replace placeholder in the message template with the actual username
        message = message_template.replace('{{username}}', username)

        try:
            # Send message to each client via Telegram using HTML formatting
            bot.send_message(chat_id=telegram_id, text=message, parse_mode=telegram.ParseMode.HTML)
            print(f"Message sent to {username} (Telegram ID: {telegram_id})")
        except Exception as e:
            print(f"Failed to send message to {telegram_id}: {e}")

if __name__ == '__main__':
    send_message_to_clients()
