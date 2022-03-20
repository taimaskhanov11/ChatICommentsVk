from collections import deque

import aioredis
from pydantic import BaseModel

from chaticommentsvk.apps.vk.classes import CommentRequest, LikeRequest, Request
from chaticommentsvk.config.config import config


class DelMessage(BaseModel):
    chat_id: int
    message_id: int


obj = Request(
    like=LikeRequest(type="post", owner_id=624187368, item_id=385),
    comment=CommentRequest(type="post", owner_id=624187368, item_id=385),
    url="https://vk.com/wall624187368_385",
)

current_posts = deque([obj], maxlen=config.bot.queue_length)
redis = aioredis.from_url(f"redis://{config.db.host}", decode_responses=True)
