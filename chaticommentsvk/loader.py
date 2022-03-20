import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.config.config import config

bot = Bot(token=config.bot.token)
dp = Dispatcher(bot, storage=RedisStorage2(config.db.host))
vk_checker = VkChecker(config.vk.token)


class TempData:
    pre_message = {}
    message_queue = asyncio.Queue()
    pre_message_task: dict[int, tuple[types.Message, asyncio.Task]] = {}
