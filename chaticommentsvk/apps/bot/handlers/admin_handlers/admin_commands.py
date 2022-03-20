import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ChatType

from chaticommentsvk.apps.bot import markups
from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import redis


class EditQueueLengthStatesGroup(StatesGroup):
    end = State()


class EditPostTypeStatesGroup(StatesGroup):
    end = State()


async def admin_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберите настройку", reply_markup=markups.admin_menu)


async def settings_menu(message: types.Message, state: FSMContext):
    await state.finish()
    answer = f"Длинна очереди:{config.bot.queue_length}\n" f"Тип постов: {config.bot.check_type}"
    await message.answer(answer, reply_markup=markups.settings_menu)


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


async def edit_queue_length(call: types.CallbackQuery):
    await call.message.answer("Введите новую длину очереди")
    await EditQueueLengthStatesGroup.first()


async def edit_queue_length_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        config.bot.queue_length = int(message.text)
        await state.finish()
        await message.answer("Длинна очереди успешно обновлена")
    else:
        await message.answer("Неправильный ввод, повторите попытку")


async def edit_post_type(call: types.CallbackQuery):
    await call.message.answer("Выберите тип постов", reply_markup=markups.post_type)
    await EditPostTypeStatesGroup.first()


async def edit_post_type_end(message: types.Message, state: FSMContext):
    if message.text in ["like", "comment", "like_comment"]:
        await message.answer("Тип постов успешно обновлен", reply_markup=markups.admin_menu)
        await state.finish()
    else:
        await message.answer("Неправильный ввод, повторите попытку")


# todo 20.03.2022 17:44 taima: добавить общий фильтр
def register_admin_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_start,
        commands="start",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )

    dp.register_message_handler(
        statistics,
        text_startswith="📉",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )
    dp.register_message_handler(
        settings_menu,
        text_startswith="⚙",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )

    dp.register_callback_query_handler(
        edit_queue_length,
        text="edit_queue_length",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )

    dp.register_message_handler(
        edit_queue_length_end,
        text="edit_queue_length",
        state=EditQueueLengthStatesGroup,
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )

    dp.register_callback_query_handler(
        edit_post_type,
        text="edit_post_type",
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )
    dp.register_message_handler(
        edit_queue_length_end,
        text="edit_post_type",
        state=EditPostTypeStatesGroup,
        chat_type=ChatType.PRIVATE,
        user_id=config.bot.admins,
    )
