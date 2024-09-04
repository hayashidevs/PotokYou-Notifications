import yaml
import os

# Load the bot token from environment variables or hardcode (for demonstration purposes)
BOT_TOKEN = 'yourtoken'

# Set up the API endpoint for fetching clients
API_BASE_URL = 'http://127.0.0.1:8000/api/clients/'  # Update with your actual Django API endpoint

# Load the message from a YAML file with UTF-8 encoding
def load_message():
    with open('bot/message.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)['message']
