from aiogram.types import ReplyKeyboardMarkup

admin_menu = ReplyKeyboardMarkup(
    [
        ["📉 Статистика бота", "⚙ Настройки бота"],
        ["👥 Настройки админов и випов"],
        [],
        ["🔩 Изменить очередь"],
    ],
    resize_keyboard=True,
)
