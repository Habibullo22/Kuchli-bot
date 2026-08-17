from telebot import TeleBot
from telebot.types import Message

from database import save_user
from telegram_client import client


def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            "👋 Salom!\n\n"
            "Telegram username yoki ID yuboring.\n"
            "Masalan: @username yoki 123456789"
        )

    @bot.message_handler(func=lambda message: True)
    def search(message: Message):
        query = message.text.strip()

        if not query:
            bot.send_message(message.chat.id, "❌ Ma'lumot kiriting.")
            return

        bot.send_message(
            message.chat.id,
            "🔎 Qidirilmoqda..."
        )

        try:
            user = client.loop.run_until_complete(
                client.get_entity(query)
            )

            username = getattr(user, "username", None)
            first_name = getattr(user, "first_name", None)
            last_name = getattr(user, "last_name", None)
            user_id = getattr(user, "id", None)

            save_user(
                user_id,
                username,
                first_name,
                last_name
            )

            username_text = (
                f"@{username}"
                if username
                else "Username yo‘q"
            )

            name = " ".join(
                x for x in [first_name, last_name]
                if x
            ) or "Ism ko‘rsatilmagan"

            text = (
                "✅ Ma'lumot topildi!\n\n"
                f"👤 Ism: {name}\n"
                f"🔗 Username: {username_text}\n"
                f"🆔 ID: {user_id}"
            )

            bot.send_message(message.chat.id, text)

        except Exception:
            bot.send_message(
                message.chat.id,
                "❌ Ma'lumot topilmadi yoki bu akkauntga "
                "kirish imkoniyati yo‘q."
          )
