import os
from telethon import TelegramClient
from config import API_ID, API_HASH

os.makedirs("sessions", exist_ok=True)

client = TelegramClient(
    "sessions/account",
    API_ID,
    API_HASH
)
