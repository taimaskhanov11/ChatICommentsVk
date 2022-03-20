import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from chaticommentsvk.apps.bot.handlers.admin_handlers.admin_commands import register_admin_commands_handlers
from chaticommentsvk.apps.bot.handlers.common_commands import register_common_handlers
from chaticommentsvk.apps.bot.utils.message_processes import message_delete_worker
from chaticommentsvk.config.log_settings import init_logging
from chaticommentsvk.loader import bot, dp


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        # BotCommand(command="/admin_start", description="Главное меню для админов"),
        # BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    init_logging(old_logger=True, level=logging.INFO, steaming=True)
    # Настройка логирования в stdout
    logger.info("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    # bot = Bot(token=TG_TOKEN)
    # dp = Dispatcher(bot, storage=MemoryStorage())
    print((await bot.get_me()).username)

    # Меню админа
    # register_admin_handlers(dp)

    # Регистрация хэндлеров
    register_common_handlers(dp)
    register_admin_commands_handlers(dp)
    # Регистрация middleware
    # dp.middleware.setup(FatherMiddleware())
    # todo 19.03.2022 17:42 taima:
    # dp.middleware.setup(ThrottlingMiddleware(limit=0.5))

    # Регистрация фильтров
    # dp.filters_factory.bind(ChatTypeFilter(chat_type=ChatType.PRIVATE), event_handlers=[all_text])

    # Установка команд бота
    await set_commands(bot)

    # Инициализация базы данных
    # await init_tortoise()

    asyncio.create_task(message_delete_worker())
    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
