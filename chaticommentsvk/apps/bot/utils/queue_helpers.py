from aiogram import types

from chaticommentsvk.apps.bot import markups
from chaticommentsvk.db.db_main import temp


async def send_current_queues(message: types.Message):
    await message.answer("Текущая очередь:\n")
    for num, q in enumerate(temp.current_posts, 1):
        await message.answer(f"{num}. {q.url}", reply_markup=markups.get_queue_keyboard(q.url))
