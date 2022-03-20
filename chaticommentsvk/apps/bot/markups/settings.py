from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


_setting_menu_buttons = [
    [ibtn("Изменить тип постов", "edit_post_type")],
    [
        ibtn("Изменить длину очереди постов", "edit_queue_length"),
    ],
]
settings_menu = InlineKeyboardMarkup(
    inline_keyboard=_setting_menu_buttons,
)

post_type = ReplyKeyboardMarkup([["like"], ["comment"], ["like_comment"]], resize_keyboard=True)
