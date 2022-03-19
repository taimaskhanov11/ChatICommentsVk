import asyncio
from collections import deque

import aioredis
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import CommentRequest, LikeRequest, Request
from chaticommentsvk.config.config import config

redis = aioredis.from_url(f"redis://{config.db.host}", decode_responses=True)

bot = Bot(token=config.bot.token)
dp = Dispatcher(bot, storage=RedisStorage2(config.db.host))
vk_checker = VkChecker(config.vk.token)

obj = Request(
    like=LikeRequest(type="post", owner_id=624187368, item_id=385),
    comment=CommentRequest(owner_id=624187368, post_id=385),
    url="https://vk.com/wall624187368_385",
)

POST_LIST = deque([obj], maxlen=config.bot.queue_length)


class TempData:
    pre_message = {}
    message_queue = asyncio.Queue()
    pre_message_task: dict[int, tuple[types.Message, asyncio.Task]] = {}

