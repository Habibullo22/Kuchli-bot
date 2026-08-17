import threading
import telebot

from config import BOT_TOKEN
from database import init_db
from handlers import register_handlers
from telegram_client import (
    client,
    start_loop,
    run_async
)


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi!")


# =========================
# DATABASE
# =========================

init_db()


# =========================
# TELEGRAM BOT
# =========================

bot = telebot.TeleBot(BOT_TOKEN)


# =========================
# TELETHON LOOP
# =========================

telegram_thread = threading.Thread(
    target=start_loop,
    daemon=True
)

telegram_thread.start()


# =========================
# TELEGRAM ACCOUNT LOGIN
# =========================

print("📱 Telegram akkaunt ulanmoqda...")

run_async(client.start())

me = run_async(client.get_me())

print()
print("================================")
print("✅ TELEGRAM AKKAUNT ULANDI")
print("================================")
print(f"👤 Ism: {me.first_name}")
print(f"🆔 ID: {me.id}")

if me.username:
    print(f"🔗 Username: @{me.username}")
else:
    print("🔗 Username: yo‘q")

print("================================")


# =========================
# BOT HANDLERS
# =========================

register_handlers(bot)


# =========================
# START BOT
# =========================

print()
print("🤖 BOT ISHGA TUSHDI...")
print("📡 Polling boshlandi...")


bot.infinity_polling(
    skip_pending=True,
    timeout=30,
    long_polling_timeout=30
)
