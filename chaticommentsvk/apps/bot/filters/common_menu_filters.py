from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from chaticommentsvk.apps.bot.utils.message_processes import message_controller
from chaticommentsvk.apps.vk.classes import Request
from chaticommentsvk.config.answer import answer
from chaticommentsvk.db.db_main import redis, temp


class PostLinkFilter(BoundFilter):
    """Проверка корректности ссылки и валидация"""

    async def check(self, message: types.Message):
        logger.trace(message)
        await redis.incr("total_messages")

        request = Request.parse_url(message)
        # Если сообщение успешно запарсено возвращаем объект запроса
        if request:

            # Проверка наличия url среди уже существующих
            logger.debug(f"Проверка наличия {request}")
            if request in temp.current_posts:  # todo 19.03.2022 15:26 taima:
                logger.trace(f"{request} уже существует")
                await message_controller(message, answer.common.link_exists)

            else:
                logger.success(f"Прошел проверку {request}")
                return {"new_request": request}

        # Если сообщение не корректно
        else:
            logger.debug(f"Некорректный ввод {message.from_user.username}|{message.text}")
            await message_controller(message, answer.common.incorrect_message)

    # todo 20.03.2022 3:09 taima:
