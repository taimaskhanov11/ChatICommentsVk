from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        pass
