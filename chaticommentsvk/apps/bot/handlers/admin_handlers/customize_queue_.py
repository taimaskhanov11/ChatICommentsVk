from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from chaticommentsvk.apps.bot import markups
from chaticommentsvk.apps.bot.utils.queue_helpers import send_current_queues
from chaticommentsvk.apps.vk.classes import Request
from chaticommentsvk.db.db_main import temp


class AddPostGroupStates(StatesGroup):
    add = State()


async def customize_queue_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await send_current_queues(message)
    await message.answer(
        "При добавлении нового поста автоматически удалиться самый первый в очереди, если очередь заполнена",
        reply_markup=markups.add_post_keyboard,
    )


async def add_post_start(call: types.CallbackQuery):
    await call.message.answer("Введите url поста")
    await AddPostGroupStates.first()


async def add_post(message: types.Message, state: FSMContext):
    request = await Request.parse_url(message)
    if request:
        temp.current_posts.append(request)
        await message.answer("Пост успешно добавлен")
        await state.finish()
    else:
        await message.answer("Не удалось добавить пост, проверьте правильность введенных данных")


async def delete_post(call: types.CallbackQuery):
    url = call.data[12:]
    for p in temp.current_posts:
        if url == p:
            await call.bot.delete_message(p.chat_id, p.message_id)
            temp.current_posts.remove(url)
            await call.message.delete()
            await call.message.answer(f"Пост {url} успешно удален")
            logger.info(f"Пост {url} удален")
            break
    # if url in temp.current_posts:
    #     temp.current_posts.remove(url)
    #     await call.message.answer("Пост успешно удален")
    #     logger.info(f"Пост {url} удален")
    else:
        await call.message.answer("Пост не найден в очереди")


def register_customize_queue_handlers(dp: Dispatcher):
    dp.register_message_handler(customize_queue_menu, text_startswith="🔩", state="*")
    dp.register_callback_query_handler(delete_post, text_startswith="delete_post")
    dp.register_callback_query_handler(add_post_start, text_startswith="add_post")
    dp.register_message_handler(add_post, state=AddPostGroupStates)
