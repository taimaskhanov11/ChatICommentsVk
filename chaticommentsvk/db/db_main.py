from aiogram import types

from chaticommentsvk.loader import bot, redis


async def message_controller(message: types.Message):
    odl_message: dict = await redis.getset(f"message_{message.from_user.id}",
                                           {"chat_id": message.chat.id, "message_id": message.message_id})
    if odl_message:
        await bot.delete_message(**odl_message)
