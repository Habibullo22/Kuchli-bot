from telebot import TeleBot
from telebot.types import Message

from config import ADMIN_ID
from menu import main_menu

from database import (
    save_user,
    get_balance
)

from telegram_client import client, run_async


def register_handlers(bot: TeleBot):

    # =========================
    # START
    # =========================

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


    # =========================
    # SEARCH BUTTON
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "🔎 Qidirish"
    )
    def search_button(message: Message):

        bot.send_message(
            message.chat.id,
            "🔎 Username yoki Telegram ID yuboring.\n\n"
            "Masalan:\n"
            "@username\n"
            "123456789"
        )


    # =========================
    # PROFILE
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "👤 Profil"
    )
    def profile(message: Message):

        user = message.from_user

        name = user.first_name or "—"

        if user.username:
            username = f"@{user.username}"
        else:
            username = "—"

        balance = get_balance(user.id)

        bot.send_message(
            message.chat.id,
            "👤 PROFIL\n\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Ism: {name}\n"
            f"🔗 Username: {username}\n"
            f"💳 Balans: {balance:,} so‘m"
        )


    # =========================
    # BALANCE
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "💳 Balans"
    )
    def balance(message: Message):

        amount = get_balance(
            message.from_user.id
        )

        bot.send_message(
            message.chat.id,
            "💳 BALANS\n\n"
            f"💰 {amount:,} so‘m"
        )


    # =========================
    # DEPOSIT
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "💰 Balansni to‘ldirish"
    )
    def deposit(message: Message):

        bot.send_message(
            message.chat.id,
            "💰 BALANSNI TO‘LDIRISH\n\n"
            "To‘lov tizimi keyingi bosqichda ulanadi."
        )


    # =========================
    # HISTORY
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "📋 Qidiruvlarim"
    )
    def history(message: Message):

        bot.send_message(
            message.chat.id,
            "📋 QIDIRUVLARIM\n\n"
            "Hozircha qidiruvlar tarixi bo‘sh."
        )


    # =========================
    # SETTINGS
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "⚙️ Sozlamalar"
    )
    def settings(message: Message):

        bot.send_message(
            message.chat.id,
            "⚙️ SOZLAMALAR\n\n"
            "Hozircha sozlamalar mavjud emas."
        )


    # =========================
    # ADMIN PANEL
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "👑 Admin panel"
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


    # =========================
    # USER SEARCH
    # =========================

    @bot.message_handler(
        func=lambda message: True
    )
    def search_user(message: Message):

        query = message.text.strip()

        if not query:
            return

        # Menyu tugmalarini qidiruvga yubormaslik
        menu_buttons = [
            "🔎 Qidirish",
            "👤 Profil",
            "📋 Qidiruvlarim",
            "💳 Balans",
            "💰 Balansni to‘ldirish",
            "⚙️ Sozlamalar",
            "👑 Admin panel"
        ]

        if query in menu_buttons:
            return

        bot.send_message(
            message.chat.id,
            "🔎 Qidirilmoqda..."
        )

        try:

            # Telegram API orqali entity olish
            user = run_async(
                client.get_entity(query)
            )

            user_id = getattr(
                user,
                "id",
                None
            )

            username = getattr(
                user,
                "username",
                None
            )

            first_name = getattr(
                user,
                "first_name",
                None
            )

            last_name = getattr(
                user,
                "last_name",
                None
            )

            save_user(
                user_id,
                username,
                first_name,
                last_name
            )

            name_parts = [
                first_name,
                last_name
            ]

            name = " ".join(
                x for x in name_parts
                if x
            )

            if not name:
                name = "—"

            if username:
                username_text = f"@{username}"
            else:
                username_text = "—"

            bot.send_message(
                message.chat.id,
                "✅ MA'LUMOT TOPILDI!\n\n"
                f"👤 Ism: {name}\n"
                f"🔗 Username: {username_text}\n"
                f"🆔 ID: {user_id}"
            )

        except Exception as e:

            print(
                f"❌ Search error: {e}"
            )

            bot.send_message(
                message.chat.id,
                "❌ Ma'lumot topilmadi.\n\n"
                "Username yoki ID noto‘g‘ri bo‘lishi "
                "mumkin yoki Telegram bu ma’lumotni "
                "olishga ruxsat bermagan."
            )
