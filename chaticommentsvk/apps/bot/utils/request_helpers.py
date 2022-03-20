import asyncio
from typing import Optional

from loguru import logger

from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import Response
from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import current_posts


async def send_check_request(checker_user: int, vk_checker: VkChecker) -> tuple:
    tasks = []
    logger.debug(f"{checker_user} -> Отправка запросов на проверку")
    for request in current_posts:
        # task = asyncio.create_task(vk_checker.is_liked_commented(checker_user, pre_request_obj))
        # todo 19.03.2022 21:20 taima: поправить отправку запроса
        task = asyncio.create_task(vk_checker.send_request(checker_user, request, config.bot.check_type))
        tasks.append(task)

    result = await asyncio.gather(*tasks)
    logger.debug(f"Весь результат|{result}")
    not_done_response: tuple[Optional[Response], ...] = tuple(filter(lambda x: not bool(x), result))
    logger.debug(f"Не выполненные задачи|{not_done_response}")
    return not_done_response
