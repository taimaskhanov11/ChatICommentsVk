import re
import typing

from pydantic import BaseModel, Field, validator
from pydantic.dataclasses import Optional


class LikeRequest(BaseModel):
    # url: str
    type: typing.Literal["post", "photo"]
    # user_id: int
    owner_id: int
    item_id: int

    # todo 19.03.2022 15:33 taima: добавить проверку остаьных полей
    # def __eq__(self, other):
    #     if isinstance(other, LikeRequest):
    #         return bool(self.url == other.url)
    #     return False


class CommentRequest(BaseModel):
    # user_id: int
    # url: str
    owner_id: int
    post_id: int = Field(alias="item_id")
    count: int = 50

    class Config:
        allow_population_by_field_name = True


class Request(BaseModel):
    url: str
    like: LikeRequest
    comment: CommentRequest

    def __eq__(self, other):
        if isinstance(other, Request):
            return bool(self.url == other.url)
        return False


class Response(BaseModel):
    url: str
    # failed: Optional[LikeRequest | CommentRequest]
    is_liked: bool
    is_commented: bool
    is_successfully: Optional[bool]

    def __bool__(self):
        return self.is_successfully

    def get_answer(self) -> str:
        match self.is_liked, self.is_commented:
            case False, False:
                answer = f"Поставить лайк и написать комментарий "
            case False, True:
                answer = f"Поставить лайк "
            case _:
                answer = f"Написать комментарий "
        answer += self.url
        return answer


async def parse_url(url: str) -> Optional[Request]:
    data: list[str] = re.findall(r"wall(.*)", url)
    if len(data) == 1:
        owner_id, item_id = data[0].split("_")
        fields = {
            "type": "post",
            # "user_id": user_id,
            "owner_id": owner_id,
            "item_id": item_id,
        }
        return Request(like=LikeRequest(**fields), comment=CommentRequest(**fields), url=url)
