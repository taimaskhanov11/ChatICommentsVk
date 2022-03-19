import asyncio
import functools
import typing

from aiovk import API, TokenSession
from loguru import logger

from chaticommentsvk.apps.vk.classes import CommentRequest, LikeRequest, Request, Response
# todo 18.03.2022 16:45 taima: Получить идентификатор комментария
# todo 18.03.2022 16:49 taima: Проверять текст комментария
from chaticommentsvk.config.config import config


class VkChecker:
    def __init__(self, token, loop=None):
        # self.driver = HttpDriver(loop=loop) if loop else None
        self.session = TokenSession(token)
        self.api = API(self.session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Закрытые сессии")
        await self.session.close()

    # todo 18.03.2022 17:57 taima: добавить проверку репоста
    async def is_liked(self, user_id, like: LikeRequest) -> bool:
        """Проверка лайка"""
        response = await self.api.likes.isLiked(user_id=user_id, **like.dict())
        logger.trace(f"Запрос is_liked|{response}")
        # is_successfully = bool(response["liked"])
        return bool(response["liked"])
        # if is_successfully:
        #     return SuccessfullyResponse(**like.dict())
        # return UnsuccessfulResponse(**like.dict())

        # return response

    # todo 18.03.2022 19:08 taima: добавить проверку комментария
    @staticmethod
    def _checking_comment(user_id, com_obj) -> bool:
        return bool(user_id == com_obj["from_id"])

    async def is_commented(self, user_id, comment: CommentRequest) -> bool:
        """Проверка комментария"""
        response = await self.api.wall.getComments(user_id=user_id, **comment.dict(exclude={"user_id"}))
        logger.trace(f"Запрос is_commented|{response}")
        # func = functools.partial(self._checking_comment, user_id)
        func = functools.partial(lambda us_id, com_obj: bool(us_id == com_obj["from_id"]), user_id)
        # is_successfully = any(map(func, response["items"]))
        return any(map(func, response["items"]))

        # if is_successfully:
        #     return SuccessfullyResponse(**comment.dict())
        # return UnsuccessfulResponse(**comment.dict())

    async def is_liked_commented(self, user_id, request: Request) -> Response:
        """Проверка комментария и лайка"""

        logger.debug(f"{request.like}|{request.comment}")
        is_liked, is_commented = await asyncio.gather(
            self.is_liked(user_id, request.like), self.is_commented(user_id, request.comment)
        )
        return Response(
            url=request.url, is_liked=is_liked, is_commented=is_commented, is_successfully=all((is_liked, is_commented))
        )

    async def send_request(
            self, user_id, request: Request, check_type: typing.Literal["like", "comment", "like_comment"]
    ) -> Response:

        is_liked, is_commented = True, True
        if check_type == "like":
            is_liked = await self.is_liked(user_id, request.like)
        elif check_type == "comment":
            is_commented = await self.is_commented(user_id, request.comment)
        else:
            is_liked, is_commented = await asyncio.gather(
                self.is_liked(user_id, request.like), self.is_commented(user_id, request.comment)
            )
        return Response(
            url=request.url, is_liked=is_liked, is_commented=is_commented, is_successfully=all((is_liked, is_commented))
        )


async def main():
    # res =await api.wall.getComment(owner_id=309981726,comment_id=309981726_632)
    item = "https://vk.com/id312730516?z=photo312730516_457273310%2Falbum312730516_0%2Frev"
    # res =await api.wall.get(owner_id=309981726)
    # res =await api.likes.getList(type="photo",owner_id=309981726, item_id=457273310)
    # res = await api.likes.getList(type="post", owner_id=-37633522, item_id=682786)
    # res = await api.likes.getList(type="post", owner_id=-37633522, item_id=682786)
    # "https://vk.com/id180142252?w=wall180142252_14730"
    # res = await api.likes.isLiked(type="post", user_id=222256657, owner_id=180142252, item_id=14730)
    "https://vk.com/id312730516?z=photo_457274394%2Falbum312730516_0%2Frev"
    # res = await api.likes.getList(type="photo", owner_id=235988501, item_id=456291834)
    # res = await api.likes.getList(type="post", owner_id=180142252, item_id=14730)
    # Проверка лайка
    # res = await api.likes.isLiked(type="post", user_id=222256657, owner_id=180142252, item_id=14730)
    # print(res)
    # Проверка comment
    # "https://vk.com/andreirozshkov?z=photo280223270_457246410%2Falbum280223270_0%2Frev"
    # res = await api.likes.isLiked(type="comment",user_id=222256657, owner_id=180142252, item_id=14730)
    # res = await api.likes.isLiked(type="comment",user_id=222256657, owner_id=280223270, item_id=3885)
    # res = await api.wall.get(type="comment",owner_id=98944499)
    # "https://vk.com/wall312730516_631"
    # res = await api.likes.getList(type="post",owner_id=312730516, item_id=631)
    # res = await api.likes.isLiked(type="post",user_id=222256657, owner_id=312730516, item_id=631)
    # res = await api.likes.isLiked(type="comment",user_id=222256657, owner_id=312730516, item_id=631)
    # "https://vk.com/wall312730516_631"

    # res = await api.wall.getComments(owner_id=312730516, post_id=631, count=50)
    # user_id = 222256657
    # url = "https://vk.com/wall312730516_631"
    checker = VkChecker(config.vk.token)
    # like, comment = parse_url(url)
    # # res = await checker.is_liked(, *parse_url("https://vk.com/wall312730516_631"))
    # res = await checker.is_commented(user_id, comment)
    #
    # pprint(res)
    print(await checker.api.users.get(user_ids="id408048349"))
    await checker.session.close()


if __name__ == "__main__":
    # asyncio.run(main())
    # parse_url("wall312730516_631")
    # exit()
    asyncio.get_event_loop().run_until_complete(main())
