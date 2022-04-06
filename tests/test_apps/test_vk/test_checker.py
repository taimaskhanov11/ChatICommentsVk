import asyncio

import pytest


@pytest.fixture
def is_access_request(self, vk_checker, vk_request):
    async def wrapper(url):
        return await asyncio.gather(
            vk_checker.is_access(self.user_id, "like", vk_request(url)),
            vk_checker.is_access(self.user_id, "comment", vk_request(url)),
            vk_checker.is_access(self.user_id, "like_comment", vk_request(url)),
        )

    return wrapper


@pytest.mark.usefixtures("remove_log")
@pytest.mark.asyncio
class TestVkChecker:
    user_id = 713503927

    @pytest.mark.parametrize("url", ("https://vk.com/id690164645?z=photo690164645_457239017%2Falbum690164645_0%2Frev",
                                     "https://vk.com/wall690164645_1",
                                     ))
    async def test_is_access_close_account(self, is_access_request, url):
        like, comment, like_comment = await is_access_request(url)
        assert all([like, comment, like_comment]) is False

    @pytest.mark.parametrize("url", ("https://vk.com/id458673263?z=photo458673263_456239029%2Falbum458673263_00%2Frev",
                                     "https://vk.com/wall458673263_33"))
    async def test_is_access_open_account(self, is_access_request, url):
        like, comment, like_comment = await is_access_request(url)
        assert all([like, comment, like_comment]) is True

    @pytest.mark.parametrize("url", ("https://vk.com/id340394219?z=photo340394219_411273010%2Falbum340394219_0%2Frev",
                                     "https://vk.com/id340394219?z=photo340394219_411259748%2Fwall340394219_1348",
                                     "https://vk.com/wall340394219_1348"))
    async def test_is_access_only_like(self, is_access_request, url):
        like, comment, like_comment = await is_access_request(url)
        assert like is True
        assert comment is False
        assert like_comment is False

    @pytest.mark.parametrize("text", ("https://vk.com/id261373355?z=photo261373355_456240002%2Fwall261373355_7595",
                                      "https://vk.com/wall261373355_7529",
                                      "https://vk.com/id261373355!!asdfasdfasdfasd",
                                      ))
    async def test_is_other_user_not_user(self, vk_checker, text):
        other_user = await vk_checker.is_other_user(text)
        assert other_user is None

    @pytest.mark.parametrize("text", ("https://vk.com/id261373355?z=photo261373355_456240002%2Fwall261373355_7595\n"
                                      "!!https://vk.com/id999999ddfg",
                                      "https://vk.com/wall261373355_7529!!https://vk.com/givemybiggyshur"))
    async def test_is_other_user_incorrect_user(self, vk_checker, text):
        other_user = await vk_checker.is_other_user(text)
        assert other_user is None

    @pytest.mark.parametrize("text, expected",
                             (("https://vk.com/id261373355?z=photo261373355_456240002%2Fwall261373355_7595\n"
                               "!!https://vk.com/id261373355", 261373355),
                              ("https://vk.com/wall261373355_7529!!https://vk.com/melt_your_heart", 222256657),
                              ("ыводфыва фывладжрфы вадфыолв арфывдлора !!https://vk.com/id261373355", 261373355),
                              ("!!https://vk.com/id690164645\n\nыводфыва фывладж \n\n\n\n!!https://vk.com/id690164645",
                               690164645),
                              )
                             )
    async def test_is_other_user_is_currect_user(self, vk_checker, text, expected):
        other_user = await vk_checker.is_other_user(text)
        assert other_user == expected
