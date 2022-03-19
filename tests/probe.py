import re
# is_liked, is_commented = await asyncio.gather(
#     vk_checker.is_liked(user_id, pre_like_request),
#     vk_checker.is_commented(user_id, pre_comment_request)
# )
# a = [(1, 0), (0, 1)]
# res = tuple(filter(lambda x: all(x), a))
# print(bool(res))
# print(list(res))
# print()
# url  = "https://vk.com/wall408048349_283\n" \
#        "!!https://vk.com/id408048349"
# data: list[str] = re.findall(r"wall(.*)", url)
# other_id = re.findall(r"!!.*vk.com/(.*)", url)
# print(data)
# print(other_id)
from typing import Optional

from pydantic import BaseModel, validator

# print(await vk_checker.is_liked(user_id, pre_like_request))
# print(await vk_checker.is_commented(user_id, pre_comment_request))

# _is_liked = functools.partial(vk_checker.is_liked, user_id)
# _is_commented = functools.partial(vk_checker.is_commented, user_id)

# is_liked = all(filter(_is_liked, POST_LIST))
# is_commented = all(filter(_is_commented, POST_LIST))
#
# print(all(list(filter(_is_liked, POST_LIST))))
# print(is_liked)
# print(is_commented)


class T(BaseModel):
    a: Optional[list]

    @validator("a")
    def get(cls, value, values):
        print(values)


t = T(a="1, 2, 3, 4")
