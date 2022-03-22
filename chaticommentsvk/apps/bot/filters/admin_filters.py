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
            obj = obj.chat
        elif isinstance(obj, types.CallbackQuery):
            obj = obj.message.chat
        elif isinstance(obj, types.ChatMemberUpdated):
            obj = obj.chat
        else:
            logger.warning("Непредвиденная ошибка")
            return False
        if obj.type == ChatType.PRIVATE and obj.id in config.bot.admins:
            return True
