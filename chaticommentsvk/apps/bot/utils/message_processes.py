import asyncio

from aiogram import types
from loguru import logger

from chaticommentsvk.db.db_main import DelMessage, redis
from chaticommentsvk.loader import TempData, bot


async def message_controller(message: types.Message, answer: str, **kwargs):
    """Удаление лишних сообщений из чата"""
    await message.delete()
    new_message = await message.answer(answer, **kwargs)

    del_message = DelMessage(chat_id=new_message.chat.id, message_id=new_message.message_id)
    old_data = await redis.getset(f"message_{del_message.chat_id}", del_message.json())
    if old_data:
        old_message = DelMessage.parse_raw(old_data)
        logger.trace(f"Удаление {old_message}")
        await bot.delete_message(**old_message.dict())


async def pre_message_process(message):
    ui = message.from_user.id
    pre_message = TempData.pre_message.get(ui)
    if pre_message:
        await pre_message.delete()
    TempData.pre_message[ui] = message


async def pre_message_process2(message):
    ui = message.from_user.id
    if TempData.pre_message_task.get(ui):
        try:
            message, task = TempData.pre_message_task[ui]
            await bot.delete_message(message.chat.id, message.message_id)
            # await message.delete()
            logger.debug(task.cancel())
            del TempData.pre_message_task[ui]
            logger.debug(f"Сообщение удалено заранее {message.message_id}|{message.from_user.id} c задачей")

        except Exception as e:
            logger.warning(e)
            pass
    await TempData.message_queue.put(message)


async def message_delete_worker():
    async def delete_message(user_id):
        await asyncio.sleep(10)
        try:
            message, task = TempData.pre_message_task[user_id]
            await bot.delete_message(message.chat.id, message.message_id)
            del TempData.pre_message_task[user_id]
            # await message.delete()
            logger.info(f"Сообщение {message.message_id}|{message.from_user.id} удалено")
        except Exception as e:
            logger.warning(e)

    while True:
        # Вытаскиваем 'рабочий элемент' из очереди.
        message = await TempData.message_queue.get()
        # Сообщаем очереди, что 'рабочий элемент' обработан.
        TempData.pre_message_task[message.from_user.id] = (
            message,
            asyncio.create_task(delete_message(message)),
        )
        logger.info("Сообщения поставлено в очередь на удаление")
        TempData.message_queue.task_done()
        # await message.answer()
