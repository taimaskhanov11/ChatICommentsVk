import asyncio
from typing import Optional

from loguru import logger

from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import Response
from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import temp


async def send_check_request(checker_user: int, vk_checker: VkChecker) -> tuple:
    tasks = []
    logger.debug(f"{checker_user} -> Отправка запросов на проверку")
    for request in temp.current_posts:
        # task = asyncio.create_task(vk_checker.is_liked_commented(checker_user, pre_request_obj))
        # todo 19.03.2022 21:20 taima: поправить отправку запроса
        task = asyncio.create_task(vk_checker.send_request(checker_user, request, config.bot.check_type))
        tasks.append(task)

    result = await asyncio.gather(*tasks)

    errors_list = []
    response_list: list[Response] = []
    for res in result:
        if isinstance(res, Response):
            response_list.append(res)
        else:
            errors_list.append(res)
            try:
                temp.current_posts.remove(res.url)
                logger.warning(f"Пост без доступа успешно удален {res}")
            except Exception as e:
                logger.critical(f"Ошибка при удалении {res}|{e}")
    logger.debug(f"Весь результат|{result}")
    logger.debug(f"Ошибки |{errors_list}")
    logger.debug(f"Пройденные посты |{response_list}")
    not_done_response: tuple[Optional[Response], ...] = tuple(filter(lambda x: not bool(x), response_list))
    logger.debug(f"Не выполненные задачи|{not_done_response}")
    return not_done_response
