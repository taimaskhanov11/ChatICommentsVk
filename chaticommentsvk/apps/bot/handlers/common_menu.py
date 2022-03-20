from aiogram import Dispatcher, types
from aiogram.types import ChatType
from loguru import logger

from chaticommentsvk.apps.bot.filters.common_menu_filters import PostLinkFilter
from chaticommentsvk.apps.bot.utils.message_processes import message_controller
from chaticommentsvk.apps.bot.utils.request_helpers import send_check_request
from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import Request, Response
from chaticommentsvk.config.answer import answer
from chaticommentsvk.config.config import config
from chaticommentsvk.db.db_main import current_posts, redis

# todo 19.03.2022 13:30 taima: удаление сообщений после определенного времени
# todo 19.03.2022 13:33 taima: проверять какие задания выполнены какие нет
# todo 19.03.2022 12:47 taima:


@logger.catch
async def all_text(message: types.Message, new_request: Request):
    try:
        logger.trace(current_posts)
        await redis.incr("total_messages")
        # Отправка запросов на проверку лайка или комментария
        async with VkChecker(config.vk.token) as vk_checker:

            # Получение проверяемого пользователя
            checker_user = await vk_checker.other_user(message.text) or new_request.like.owner_id

            # Проверка доступности
            if not await vk_checker.is_access(checker_user, config.bot.check_type, new_request):
                await message_controller(message, answer.common.no_access)

            else:
                unfinished_tasks: tuple[Response] = await send_check_request(checker_user, vk_checker)

                # Если лайк или комментарий не найден
                if unfinished_tasks:
                    unfulfilled_s = answer.common.check_failed
                    # todo 19.03.2022 14:37 taima: enumarate
                    for task in unfinished_tasks:
                        # todo 19.03.2022 21:25 taima: пофиксить проверку
                        unfulfilled_s += f"{task.unfulfilled}\n"
                    await message_controller(message, unfulfilled_s, disable_web_page_preview=True)

                # Если лайк или комментарий найден добавляем в список
                else:
                    # await message.edit_text(message.text, disable_web_page_preview=True)
                    await redis.incr("post_count")
                    current_posts.append(new_request)

    except Exception as e:
        logger.critical(e)
        await message_controller(message, answer.common.error)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(all_text, PostLinkFilter(), chat_type=ChatType.SUPERGROUP)
