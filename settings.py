import os
from dotenv import load_dotenv

load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")


MESSAGE_DELETE_TIME = 5.0