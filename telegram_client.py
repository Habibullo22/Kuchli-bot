import os
import asyncio
from telethon import TelegramClient

from config import API_ID, API_HASH


os.makedirs("sessions", exist_ok=True)

client = TelegramClient(
    "sessions/account",
    API_ID,
    API_HASH
)

telegram_loop = asyncio.new_event_loop()


def start_loop():
    asyncio.set_event_loop(telegram_loop)
    telegram_loop.run_forever()


def run_async(coro):
    future = asyncio.run_coroutine_threadsafe(
        coro,
        telegram_loop
    )
    return future.result()
