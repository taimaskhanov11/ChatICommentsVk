from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from chaticommentsvk.apps.bot.utils.message_processes import message_controller
from chaticommentsvk.apps.vk.classes import parse_url
from chaticommentsvk.db.db_main import current_posts


class MainPaymentFilter(BoundFilter):
    """Проверка корректности ссылки"""

    async def check(self, message: types.Message):
        request_obj = await parse_url(message.text)

        # Если сообщение успешно запарсено возвращаем объект запроса
        if request_obj:

            # Проверка наличия url среди уже существующих
            logger.debug(f"Проверка наличия {request_obj}")
            if request_obj in current_posts:  # todo 19.03.2022 15:26 taima:
                answer = (
                    f"✅ @{message.from_user.username} эта ссылка уже есть в списке,"
                    f" дождитесь пока пройдет 5 заданий."
                )
                await message_controller(message, answer)
                return

            return {"request_obj": request_obj}

        # Если сообщение не корректно
        else:
            answer = (
                f"⛔️ @{message.from_user.username}, здесь публикуются только ссылки на пост из Вконтакте."
                f" Ознакомьтесь с правилами чата, они находятся в закрепе."
            )
            await message_controller(message, answer)

    # todo 20.03.2022 3:09 taima:
