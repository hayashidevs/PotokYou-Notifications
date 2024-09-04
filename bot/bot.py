import asyncio
import telegram
from telegram.ext import Application
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from config import BOT_TOKEN, API_BASE_URL, load_message

async def fetch_clients():
    """
    Fetch clients from the Django REST API asynchronously.
    """
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()  # Return the list of clients in JSON format
    except requests.RequestException as e:
        print(f"Failed to fetch client data: {e}")
        return []

async def send_message_to_clients(application):
    """
    Fetch clients and send them a message via Telegram asynchronously.
    """
    message_template = load_message()
    clients = await fetch_clients()

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
            await application.bot.send_message(chat_id=telegram_id, text=message, parse_mode=telegram.constants.ParseMode.HTML)
            print(f"Message sent to {username} (Telegram ID: {telegram_id})")
        except Exception as e:
            print(f"Failed to send message to {telegram_id}: {e}")

    print("All messages sent successfully!")

async def main():
    # Initialize the Telegram bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Initialize the bot
    await application.initialize()

    # Ask the user in the CMD whether to send messages
    while True:
        action = input("What do you want to do? (send/exit): ").lower()

        if action == "send":
            await send_message_to_clients(application)

        elif action == "exit":
            print("Exiting...")
            break

        else:
            print("Invalid input. Please type 'send' or 'exit'.")

    # Shut down the application
    await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
