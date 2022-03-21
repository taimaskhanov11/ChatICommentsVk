from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message):
        logger.debug(message)
