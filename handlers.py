from telebot import TeleBot
from telebot.types import Message

from config import ADMIN_ID
from menu import main_menu
from database import save_user, get_balance
from payments import create_payment
from telegram_client import client


def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def start(message: Message):
        user = message.from_user

        save_user(
            user.id,
            user.username,
            user.first_name,
            user.last_name
        )

        is_admin = user.id == ADMIN_ID

        bot.send_message(
            message.chat.id,
            "👋 Assalomu alaykum!\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu(is_admin)
        )

    @bot.message_handler(
        func=lambda message: message.text == "🔎 Qidirish"
    )
    def search_button(message: Message):
        bot.send_message(
            message.chat.id,
            "🔎 Username yoki Telegram ID yuboring.\n\n"
            "Masalan:\n"
            "@username\n"
            "123456789"
        )

    @bot.message_handler(
        func=lambda message: message.text == "👤 Profil"
    )
    def profile(message: Message):
        user = message.from_user

        name = user.first_name or "—"

        username = (
            f"@{user.username}"
            if user.username
            else "—"
        )

        balance = get_balance(user.id)

        bot.send_message(
            message.chat.id,
            "👤 Profilingiz\n\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Ism: {name}\n"
            f"🔗 Username: {username}\n"
            f"💳 Balans: {balance:,} so‘m"
        )

    @bot.message_handler(
        func=lambda message: message.text == "💳 Balans"
    )
    def balance(message: Message):
        amount = get_balance(message.from_user.id)

        bot.send_message(
            message.chat.id,
            f"💳 Sizning balansingiz:\n\n"
            f"💰 {amount:,} so‘m"
        )

    @bot.message_handler(
        func=lambda message: message.text == "💰 Balansni to‘ldirish"
    )
    def deposit(message: Message):
        bot.send_message(
            message.chat.id,
            "💰 Balansni to‘ldirish\n\n"
            "Hozircha to‘lov usulini tanlash funksiyasi "
            "tayyorlanmoqda.\n\n"
            "Keyingi bosqichda Humo / Uzcard / boshqa "
            "to‘lov usullarini ulaymiz."
        )

    @bot.message_handler(
        func=lambda message: message.text == "📋 Qidiruvlarim"
    )
    def history(message: Message):
        bot.send_message(
            message.chat.id,
            "📋 Qidiruvlar tarixi\n\n"
            "Hozircha qidiruvlar tarixi bo‘sh."
        )

    @bot.message_handler(
        func=lambda message: message.text == "⚙️ Sozlamalar"
    )
    def settings(message: Message):
        bot.send_message(
            message.chat.id,
            "⚙️ Sozlamalar\n\n"
            "Hozircha sozlamalar mavjud emas."
        )

    @bot.message_handler(
        func=lambda message: message.text == "👑 Admin panel"
    )
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
            "💳 To‘lovlarni boshqarish\n"
            "👥 Foydalanuvchilar\n"
            "📊 Statistika"
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
