from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.config.config import config

bot = Bot(token=config.bot.token)
storage = MemoryStorage() if config.db.storage == "mem" else RedisStorage2(config.db.host)
dp = Dispatcher(bot, storage=storage)
vk_checker = VkChecker(config.vk.token)
