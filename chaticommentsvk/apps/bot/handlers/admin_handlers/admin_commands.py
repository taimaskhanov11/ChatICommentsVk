import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from chaticommentsvk.apps.bot import markups
from chaticommentsvk.apps.bot.filters.admin_filters import AdminPrivateFilter
from chaticommentsvk.db.db_main import redis


async def admin_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберите настройку", reply_markup=markups.admin_menu)


async def statistics(message: types.Message):
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
        f"Всего полученных сообщений: {total_messages}",
        reply_markup=markups.admin_menu,
    )


# todo 20.03.2022 17:44 taima: добавить общий фильтр
def register_admin_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_start, AdminPrivateFilter(), commands="start", state="*")
    dp.register_message_handler(
        statistics,
        AdminPrivateFilter(),
        text_startswith="📉",
    )
    # dp.register_message_handler(
    #     admin_start,
    #     AdminPrivateFilter(),
    # )
