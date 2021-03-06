import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from chaticommentsvk.apps.bot.handlers.admin_handlers.admin_commands import register_admin_commands_handlers
from chaticommentsvk.apps.bot.handlers.admin_handlers.bot_settings import register_bot_settings_handlers
from chaticommentsvk.apps.bot.handlers.admin_handlers.customize_queue_ import register_customize_queue_handlers
from chaticommentsvk.apps.bot.handlers.admin_handlers.privilege_settings import register_privilege_handlers
from chaticommentsvk.apps.bot.handlers.common_menu import register_common_handlers
from chaticommentsvk.apps.bot.handlers.errors_handlers import register_error_handlers
from chaticommentsvk.config.config import config
from chaticommentsvk.config.log_settings import init_logging
from chaticommentsvk.db.db_main import redis
from chaticommentsvk.loader import bot, dp


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования
    init_logging(old_logger=True, level=logging.INFO, steaming=False)
    logger.info(f"Starting bot {(await bot.get_me()).username}")
    # Очистка базы перед запуском
    if config.bot.startup_clear:
        await redis.flushall()

    # Установка команд бота
    await set_commands(bot)

    # Меню админа
    register_admin_commands_handlers(dp)
    register_bot_settings_handlers(dp)
    register_privilege_handlers(dp)
    register_customize_queue_handlers(dp)

    # Хендлер ошибок
    register_error_handlers(dp)
    # Регистрация хэндлеров
    register_common_handlers(dp)
    # Регистрация middleware
    # dp.middleware.setup(FatherMiddleware())
    # todo 19.03.2022 17:42 taima:
    # dp.middleware.setup(ThrottlingMiddleware(limit=0.5))

    # Регистрация фильтров
    # dp.filters_factory.bind(chat_type=ChatType.PRIVATE, user_id=config.bot.admins,event_handlers=admin_start )

    # asyncio.create_task(message_delete_worker())

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
