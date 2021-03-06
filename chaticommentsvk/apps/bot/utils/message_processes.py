import asyncio

from aiogram import types
from loguru import logger

from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import DelMessage, redis, temp
from chaticommentsvk.loader import bot


async def message_controller(message: types.Message, answer: str, **kwargs):
    """Удаление лишних сообщений из чата"""
    await message.delete()
    new_message = await message.answer(answer.format(username=message.from_user.username), **kwargs)

    del_message = DelMessage(
        chat_id=new_message.chat.id, message_id=new_message.message_id, user_id=message.from_user.id
    )
    asyncio.create_task(delete_message_task(del_message))
    old_data = await redis.getset(f"message_{del_message.user_id}", del_message.json())
    if old_data:
        old_message = DelMessage.parse_raw(old_data)
        logger.debug(
            f"Сообщение для удаления {old_message} -- "
            f"Полученное сообщение {message.from_user.id}|{message.chat.id}|{message.message_id}"
        )
        try:
            logger.trace(f"Удаление старого {old_message}")
            await bot.delete_message(**old_message.dict(exclude={"user_id"}))
            logger.trace(f"Старое сообщение успешно удалено {old_message}")
        except Exception as e:
            logger.warning(f"Старое сообщение уже удалено|{e}")


async def delete_message_task(del_message: DelMessage):
    logger.trace(f"В очередь на удаление {del_message}")
    await asyncio.sleep(config.bot.dd_messages)
    try:
        logger.trace(f"Удаление по истечению срока {del_message}")
        await bot.delete_message(**del_message.dict(exclude={"user_id"}))
        logger.debug(f"Сообщение {del_message} успешно очищено")
    except Exception as e:
        logger.warning(f"{e}|Сообщение по истечению срока уже удалено")


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
            message, task = temp.pre_message_task[user_id]
            await bot.delete_message(message.chat.id, message.message_id)
            del TempData.pre_message_task[user_id]
            # await message.delete()
            logger.info(f"Сообщение {message.message_id}|{message.from_user.id} удалено")
        except Exception as e:
            logger.warning(e)

    while True:
        # Вытаскиваем 'рабочий элемент' из очереди.
        message = await temp.message_queue.get()
        # Сообщаем очереди, что 'рабочий элемент' обработан.
        temp.pre_message_task[message.from_user.id] = (
            message,
            asyncio.create_task(delete_message(message)),
        )
        logger.info("Сообщения поставлено в очередь на удаление")
        TempData.message_queue.task_done()
        # await message.answer()
