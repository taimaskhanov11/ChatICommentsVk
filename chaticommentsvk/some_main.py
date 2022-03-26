import asyncio
import logging
from multiprocessing import Process
from pathlib import Path

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from chaticommentsvk.config.config import BASE_DIR, load_yaml, Config
from chaticommentsvk.config.log_settings import init_logging


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def main(config_path):
    from chaticommentsvk.config import config

    config.config = Config(**load_yaml(config_path))
    from loguru import logger
    from chaticommentsvk.apps.bot.handlers.admin_handlers.admin_commands import register_admin_commands_handlers
    from chaticommentsvk.apps.bot.handlers.admin_handlers.bot_settings import register_bot_settings_handlers
    from chaticommentsvk.apps.bot.handlers.admin_handlers.privilege_settings import register_privilege_handlers
    from chaticommentsvk.apps.bot.handlers.common_menu import register_common_handlers
    from chaticommentsvk.db.db_main import redis
    from chaticommentsvk.loader import bot, dp

    # Настройка логирования
    init_logging(filename=config_path.stem, old_logger=True, level=logging.DEBUG, steaming=False)
    logger.trace(f"Starting bot {(await bot.get_me()).username}")
    # Очистка базы перед запуском
    if config.config.bot.startup_clear:
        await redis.flushall()

    # Установка команд бота
    await set_commands(bot)
    # Меню админа
    register_admin_commands_handlers(dp)
    register_bot_settings_handlers(dp)
    register_privilege_handlers(dp)

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


def process_main(config_path: Path):
    asyncio.run(main(config_path))


def processes_start():
    init_logging(old_logger=True, level=logging.INFO, steaming=True)
    config_files = []
    for file in BASE_DIR.iterdir():
        if "config" in file.name and file.suffix == ".yml":
            config_files.append(file)
            logger.success(file)

    for config_file in config_files:
        Process(target=process_main, args=(config_file,)).start()


if __name__ == "__main__":
    processes_start()
