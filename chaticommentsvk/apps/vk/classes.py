import re
import typing

from aiogram import types
from pydantic import BaseModel, Field, validator
from pydantic.dataclasses import Optional


# class BaseRequest(BaseModel):
#     type: #typing.Literal["post", "photo"]
#     owner_id: int
#     item_id: int


class LikeRequest(BaseModel):
    """Запрос на проверку лайка"""

    type: typing.Literal["post", "photo"]
    owner_id: int
    item_id: int


class CommentRequest(LikeRequest):
    """Запрос на проверку комментария"""

    count: Optional[int] = 50
    photo_id: Optional[int] = Field(const=True)
    post_id: Optional[int] = Field(const=True)

    @validator("photo_id", "post_id", always=True)
    def get_item_id(cls, value, values):
        return values.get("item_id")


class Request(BaseModel):
    url: str
    like: LikeRequest
    comment: CommentRequest
    chat_id: int
    message_id: int

    def __eq__(self, other):
        if isinstance(other, Request):
            return self.url == other.url
        return self.url == other

    @classmethod
    async def parse_url(cls, message: types.Message) -> Optional["Request"]:
        url = message.text
        # data: list[str] = re.findall(r"wall(.*)", url)
        data: list[str] = re.findall(r"(\bwall|\bphoto)(-?\d+_\d+)", url)
        if len(data) == 1:
            _type, item_data = data[0][0], data[0][1].split("_")
            owner_id, item_id = item_data
            item_type = "post" if _type == "wall" else _type
            fields = {
                "type": item_type,
                "owner_id": owner_id.strip(),
                "item_id": item_id.strip(),
            }
            return cls(
                like=LikeRequest(**fields),
                comment=CommentRequest(**fields),
                url=f"https://vk.com/{_type}{owner_id}_{item_id}",
                chat_id=message.chat.id,
                message_id=message.message_id,
            )


class Response(BaseModel):
    url: str
    # failed: Optional[LikeRequest | CommentRequest]
    is_liked: bool
    is_commented: bool
    is_successfully: Optional[bool]

    def __bool__(self):
        return self.is_successfully

    @property
    def unfulfilled(self) -> str:
        match self.is_liked, self.is_commented:
            case False, False:
                answer = f"Поставить лайк и написать комментарий "
            case False, True:
                answer = f"Поставить лайк "
            case _:
                answer = f"Написать комментарий "
        answer += self.url
        return answer


if __name__ == "__main__":
    b = CommentRequest(type="photo", owner_id=1, item_id=1, photo_id=1)
    print(b.dict(exclude_defaults=False))
    print(b.photo_id)
    b.photo_id = 2
