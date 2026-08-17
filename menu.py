from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(is_admin=False):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        KeyboardButton("🔎 Qidirish"),
        KeyboardButton("👤 Profil")
    )

    markup.row(
        KeyboardButton("📋 Qidiruvlarim"),
        KeyboardButton("💳 Balans")
    )

    markup.row(
        KeyboardButton("💰 Balansni to‘ldirish"),
        KeyboardButton("⚙️ Sozlamalar")
    )

    if is_admin:
        markup.row(
            KeyboardButton("👑 Admin panel")
        )

    return markup
