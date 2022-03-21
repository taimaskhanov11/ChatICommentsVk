from collections import deque

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loguru import logger

from chaticommentsvk.apps.bot import markups
from chaticommentsvk.apps.bot.filters.admin_filters import AdminPrivateFilter
from chaticommentsvk.apps.bot.utils.admin_helpers import settings_status
from chaticommentsvk.config import config
from chaticommentsvk.db.db_main import temp, obj


class EditSetStatesGroup(StatesGroup):
    queue_length = State()
    post_type = State()


class EditPostTypeStatesGroup(StatesGroup):
    end = State()


async def bot_settings_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(settings_status(), reply_markup=markups.settings_menu)


async def edit_queue_length(call: types.CallbackQuery):
    await call.message.answer("Изменение длинны очистит текущие посты\nВведите новую длину очереди")
    await EditSetStatesGroup.queue_length.set()


@logger.catch
async def edit_queue_length_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.finish()
        config.bot.queue_length = int(message.text)
        temp.current_posts = deque(maxlen=int(message.text))
        await message.answer(
            f"Длинна очереди успешно обновлена\n{settings_status()}", reply_markup=markups.settings_menu
        )
    else:
        await message.answer("Неправильный ввод, повторите попытку")


async def edit_post_type(call: types.CallbackQuery):
    await call.message.answer("Выберите тип постов", reply_markup=markups.post_type)
    await EditSetStatesGroup.post_type.set()


@logger.catch
async def edit_post_type_end(message: types.Message, state: FSMContext):
    if message.text in ["like", "comment", "like_comment"]:
        await state.finish()
        config.bot.check_type = message.text
        await message.answer(f"Тип постов успешно обновлен\n{settings_status()}", reply_markup=markups.settings_menu)
    else:
        await message.answer("Неправильный ввод, повторите попытку")


def register_bot_settings_handlers(dp: Dispatcher):
    dp.register_message_handler(
        bot_settings_menu,
        AdminPrivateFilter(),
        text_startswith="⚙",
    )

    dp.register_callback_query_handler(
        edit_queue_length,
        AdminPrivateFilter(),
        text="edit_queue_length",
    )

    dp.register_message_handler(
        edit_queue_length_end,
        AdminPrivateFilter(),
        state=EditSetStatesGroup.queue_length,
    )
    dp.register_callback_query_handler(
        edit_post_type,
        AdminPrivateFilter(),
        text="edit_post_type",
    )
    dp.register_message_handler(
        edit_post_type_end,
        AdminPrivateFilter(),
        state=EditSetStatesGroup.post_type,
    )
