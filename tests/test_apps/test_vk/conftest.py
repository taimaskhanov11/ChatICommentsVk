import asyncio
import logging
from unittest.mock import Mock

import pytest
from loguru import logger

from chaticommentsvk.apps.vk.checker import VkChecker
from chaticommentsvk.apps.vk.classes import Request


@pytest.fixture(scope='module')
def remove_log():
    logger.remove()


@pytest.fixture(scope='module')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    logger.debug("Получение цикла событий")
    loop = asyncio.get_event_loop_policy().new_event_loop()
    # loop = asyncio.get_event_loop()
    yield loop
    logger.debug("Закрытие цикла событий")
    loop.close()


# @pytest.fixture(scope='session')
# def loop():
#     return asyncio.get_event_loop()

@pytest.fixture()
async def vk_checker():
    token = "883456347cbbb2f708a41e2a96f0c7b70e3a8b02a569ecb955af86f977d379f33c1373118f9eebff11e82"
    logger.debug("Начало сессии")
    checker = VkChecker(token)
    yield checker
    logger.debug("Закрытие сессии")
    await checker.session.close()


@pytest.fixture
def vk_request():
    def get_message(url):
        message = Mock()
        message.chat.id = 1
        message.message_id = 1
        message.text = url
        request = Request.parse_url(message)
        return request

    return get_message

