from aiogram import types
from aiogram.dispatcher.filters import BoundFilter, ChatTypeFilter
from aiogram.types import ChatType
from loguru import logger

from chaticommentsvk.config.config import config


class AdminSuperGroupFilter(BoundFilter):
    pass


class AdminPrivateFilter(BoundFilter):
    async def check(self, obj: types.Message | types.CallbackQuery):
        if isinstance(obj, types.Message):
            chat = obj.chat
        elif isinstance(obj, types.CallbackQuery):
            chat = obj.message.chat
        elif isinstance(obj, types.ChatMemberUpdated):
            chat = obj.chat
        else:
            logger.warning("Непредвиденная ошибка")
            return False
        if chat.type == ChatType.PRIVATE and obj.from_user.id in config.bot.admins:
            return True
