from aiogram import Dispatcher, types
from aiogram.types import ChatType

from chaticommentsvk.config.config import config


async def admin_start(message: types.Message):
    print(message)


def register_admin_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start,
        commands="start",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )
