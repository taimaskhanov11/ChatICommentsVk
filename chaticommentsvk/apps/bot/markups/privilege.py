from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


_privilege_menu_buttons = [
    [
        ibtn("Добавить админа", "add_admin"),
        ibtn("Удалить админа", "delete_admin"),
    ],
    [
        ibtn("Добавить випа", "add_vip"),
        ibtn("Удалить випа", "delete_vip"),
    ],
]
privilege_menu = InlineKeyboardMarkup(
    inline_keyboard=_privilege_menu_buttons,
)
