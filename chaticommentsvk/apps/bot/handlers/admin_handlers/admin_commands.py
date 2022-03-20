import asyncio

from aiogram import Dispatcher, types
from aiogram.types import ChatType

from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import redis


async def admin_start(message: types.Message):
    (post_count, is_liked_requests, is_commented_requests, total_messages) = await asyncio.gather(
        redis.get("post_count"),
        redis.get("is_liked_requests"),
        redis.get("is_commented_requests"),
        redis.get("total_messages"),
    )
    await message.answer(
        f"Количество обработанных постов: {post_count}\n"
        f"Все запросов проверки лайка к VK API: {is_liked_requests}\n"
        f"Все запросов проверки комментария к VK API: {is_commented_requests}\n"
        f"Всего полученных сообщений: {total_messages}"
    )


def register_admin_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start,
        commands="start",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )
