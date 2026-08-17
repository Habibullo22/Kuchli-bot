 from telebot import TeleBot
from telebot.types import Message

from config import ADMIN_ID
from menu import main_menu
from database import save_user
from telegram_client import client


def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def start(message: Message):
        is_admin = message.from_user.id == ADMIN_ID

        bot.send_message(
            message.chat.id,
            "👋 Assalomu alaykum!\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu(is_admin)
        )

    @bot.message_handler(func=lambda message: message.text == "🔎 Qidirish")
    def search_button(message: Message):
        bot.send_message(
            message.chat.id,
            "🔎 Username yoki Telegram ID yuboring.\n\n"
            "Masalan:\n"
            "@username\n"
            "123456789"
        )


    @bot.message_handler(func=lambda message: message.text == "👤 Profil")
    def profile(message: Message):
        user = message.from_user

        bot.send_message(
            message.chat.id,
            f"👤 Sizning profilingiz\n\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Ism: {user.first_name or '—'}\n"
            f"🔗 Username: "
            f"@{user.username}" if user.username else
            f"🔗 Username: —"
        )


    @bot.message_handler(func=lambda message: message.text == "💳 Balans")
    def balance(message: Message):
        bot.send_message(
            message.chat.id,
            "💳 Balansingiz: 0 so‘m"
        )


    @bot.message_handler(func=lambda message: message.text == "💰 Balansni to‘ldirish")
    def deposit(message: Message):
        bot.send_message(
            message.chat.id,
            "💰 Balansni to‘ldirish bo‘limi\n\n"
            "To‘lov tizimi keyingi bosqichda ulanadi."
        )


    @bot.message_handler(func=lambda message: message.text == "📋 Qidiruvlarim")
    def history(message: Message):
        bot.send_message(
            message.chat.id,
            "📋 Hozircha qidiruvlar tarixi bo‘sh."
        )


    @bot.message_handler(func=lambda message: message.text == "⚙️ Sozlamalar")
    def settings(message: Message):
        bot.send_message(
            message.chat.id,
            "⚙️ Sozlamalar\n\n"
            "Hozircha sozlamalar mavjud emas."
        )


    @bot.message_handler(func=lambda message: message.text == "👑 Admin panel")
    def admin_panel(message: Message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(
                message.chat.id,
                "❌ Sizda admin huquqi yo‘q."
            )
            return

        bot.send_message(
            message.chat.id,
            "👑 ADMIN PANEL\n\n"
            "⚙️ Admin funksiyalari keyingi bosqichda qo‘shiladi."
        )


    @bot.message_handler(func=lambda message: True)
    def search_user(message: Message):

        query = message.text.strip()

        if not query:
            return

        bot.send_message(
            message.chat.id,
            "🔎 Qidirilmoqda..."
        )

        try:
            user = client.loop.run_until_complete(
                client.get_entity(query)
            )

            user_id = getattr(user, "id", None)
            username = getattr(user, "username", None)
            first_name = getattr(user, "first_name", None)
            last_name = getattr(user, "last_name", None)

            save_user(
                user_id,
                username,
                first_name,
                last_name
            )

            name = " ".join(
                x for x in [first_name, last_name]
                if x
            ) or "—"

            username_text = (
                f"@{username}"
                if username
                else "—"
            )

            bot.send_message(
                message.chat.id,
                "✅ Ma’lumot topildi!\n\n"
                f"👤 Ism: {name}\n"
                f"🔗 Username: {username_text}\n"
                f"🆔 ID: {user_id}"
            )

        except Exception as e:
            print("Search error:", e)

            bot.send_message(
                message.chat.id,
                "❌ Ma’lumot topilmadi yoki Telegram "
                "bu ma’lumotni olishga ruxsat bermadi."
            )
