import asyncio
from typing import Optional

from aiogram import Dispatcher, types
from aiogram.types import ChatType
from loguru import logger

from chaticommentsvk.apps.bot.utils.message_processes import message_controller, pre_message_process
from chaticommentsvk.apps.bot.utils.request_helpers import send_check_request
from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import Request, Response, parse_url
from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import current_posts, redis

# todo 19.03.2022 13:30 taima: удаление сообщений после определенного времени
# todo 19.03.2022 13:33 taima: проверять какие задания выполнены какие нет
# todo 19.03.2022 12:47 taima:


@logger.catch
async def all_text(message: types.Message, request_obj: Request):
    logger.trace(current_posts)
    await redis.incr("total_messages")

    # Отправка запросов на проверку лайка или комментария
    async with VkChecker(config.vk.token) as vk_checker:
        checker_user = await vk_checker.parse_checker_user(message.text) or request_obj.like.owner_id
        unfinished_tasks: tuple[Response] = await send_check_request(checker_user, vk_checker)

        # Если лайк  или комментарий не найден
        if unfinished_tasks:
            answer = f"@{message.from_user.username}, Ваш пост удален! Пройдите, пожалуйста:\n"
            # todo 19.03.2022 14:37 taima: enumarate
            for task in unfinished_tasks:
                # todo 19.03.2022 21:25 taima: пофиксить проверку
                answer += f"{task.get_answer()}\n"
            await message_controller(message, answer, disable_web_page_preview=True)

        # Если лайк или комментарий найден добавляем в список
        else:
            await redis.incr("post_count")
            current_posts.append(request_obj)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(all_text, chat_type=ChatType.SUPERGROUP)
