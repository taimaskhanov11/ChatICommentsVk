from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


_add_post_buttons = [
    [ibtn("Добавить новый пост", "add_post")],
    # [ibtn("Изменить длину очереди постов", "edit_queue_length"), ],
]

add_post_keyboard = InlineKeyboardMarkup(
    inline_keyboard=_add_post_buttons,
)


def get_queue_keyboard(url):
    _queue_button = [[ibtn("Удалить", f"delete_post_{url}")]]
    _queue_keyboard = InlineKeyboardMarkup(
        inline_keyboard=_queue_button,
    )
    return _queue_keyboard
