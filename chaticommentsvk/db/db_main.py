import asyncio
import collections
from collections import deque

import aioredis
from aiogram import types
from pydantic import BaseModel

from chaticommentsvk.apps.vk.classes import CommentRequest, LikeRequest, Request
from chaticommentsvk.config.config import config


class DelMessage(BaseModel):
    chat_id: int
    message_id: int
    user_id: int


obj = Request(
    like=LikeRequest(type="post", owner_id=624187368, item_id=385),
    comment=CommentRequest(type="post", owner_id=624187368, item_id=385),
    url="https://vk.com/wall624187368_385",
    chat_id=1,
    message_id=2,
)


class temp:
    pre_message = {}
    message_queue = asyncio.Queue()
    pre_message_task: dict[int, tuple[types.Message, asyncio.Task]] = {}
    current_posts: deque[Request] = deque(maxlen=config.bot.queue_length)


class DummyRedis:
    storage = collections.defaultdict(int)

    async def get(self, key):
        return self.storage.get(key)

    async def incr(self, key):
        self.storage[key] += 1

    async def getset(self, key, value):
        old_val = self.storage.get(key)
        self.storage[key] = value
        return old_val


redis = (
    DummyRedis()
    if config.db.storage == "mem"
    else aioredis.from_url(f"redis://{config.db.host}", decode_responses=True)
)
