import asyncio
from typing import Optional

from aiogram import Dispatcher, types
from aiogram.types import ChatType
from loguru import logger

from chaticommentsvk.apps.bot.utils.message_processes import pre_message_process
from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import Response, parse_checker_user, parse_url
from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import message_controller
from chaticommentsvk.loader import POST_LIST, TempData, redis


# todo 19.03.2022 13:30 taima: удаление сообщений после определенного времени
# todo 19.03.2022 13:33 taima: проверять какие задания выполнены какие нет
# todo 19.03.2022 12:47 taima:


@logger.catch
async def all_text(message: types.Message):
    logger.trace(POST_LIST)
    # Проверка корректности сообщения и парс данных
    request_obj = await parse_url(message.text)

    # Если сообщение успешно запарсено
    if request_obj:

        logger.debug(f"Проверка наличия {request_obj}")
        # Проверка наличия url среди уже существующих
        if request_obj in POST_LIST:  # todo 19.03.2022 15:26 taima:
            await message.delete()
            answer_message = await message.answer(
                f"✅ @{message.from_user.username} эта ссылка уже есть в списке, дождитесь пока пройдет 5 заданий."
            )
            await message_controller(answer_message)
            return

        # Отправка запросов на проверку лайка или комментария
        async with VkChecker(config.vk.token) as vk_checker:
            checker_user = await parse_checker_user(message.text, vk_checker) or request_obj.like.owner_id

            tasks = []
            for pre_request_obj in POST_LIST:
                # task = asyncio.create_task(vk_checker.is_liked_commented(checker_user, pre_request_obj))
                # todo 19.03.2022 21:20 taima: поправить отправку запроса
                task = asyncio.create_task(
                    vk_checker.send_request(checker_user, pre_request_obj, config.bot.check_type)
                )

                tasks.append(task)

            result = await asyncio.gather(*tasks)
            logger.debug(f"Весь ответ|{result}")
            not_done_response: tuple[Optional[Response], ...] = tuple(filter(lambda x: not bool(x), result))
            logger.debug(f"Не выполненные задачи|{not_done_response}")

            # Если лайк  или комментарий не найден
            if not_done_response:
                answer = f"@{message.from_user.username}, Ваш пост удален! Пройдите, пожалуйста:\n"
                # todo 19.03.2022 14:37 taima: enumarate
                for response_obj in not_done_response:
                    # todo 19.03.2022 21:25 taima: пофиксить проверку
                    if not any((response_obj.is_liked, response_obj.is_commented)):
                        answer += f"Поставить лайк и написать комментарий {response_obj.url}\n"
                    elif not response_obj.is_liked:
                        answer += f"Поставить лайк {response_obj.url}\n"
                    else:
                        answer += f"Написать комментарий {response_obj.url}\n"
                await message.delete()
                answer_message = await message.answer(answer, disable_web_page_preview=True)
                await message_controller(answer_message)

            # Если лайк или комментарий найден добавляем в список
            else:
                await redis.incr("post_count")
                POST_LIST.append(request_obj)

    # Если сообщение не корректно
    else:
        # todo 19.03.2022 12:50 taima:
        await message.delete()
        await pre_message_process(
            await message.answer(
                f"⛔️ @{message.from_user.username}, здесь публикуются только ссылки на пост из Вконтакте."
                " Ознакомьтесь с правилами чата, они находятся в закрепе.",
            )
        )


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(all_text, chat_type=ChatType.SUPERGROUP)
