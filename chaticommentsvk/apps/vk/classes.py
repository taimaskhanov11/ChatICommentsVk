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

    # @validator("is_successfully", always=True)
    # def is_successfully_check(cls, value, values):
    #     if values["is_liked"] and values["is_commented"]:
    #         return True
    #     return False


class SuccessfullyResponse(BaseModel):
    url: str

    def __bool__(self):
        return True


class UnsuccessfulResponse(BaseModel):
    url: str

    def __bool__(self):
        return False


# todo 19.03.2022 14:53 taima:
# class Response(BaseModel):
#     like: LikeRequest
#     comment: CommentRequest
#     fail_request: LikeRequest | CommentRequest
#     status: bool
#
#     def __bool__(self):
#         return self.status


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


async def parse_checker_user(text, checker) -> Optional[int]:
    checker_data = re.findall(r"!!.*vk.com/(.*)", text)
    if checker_data:
        res = await checker.api.users.get(user_ids=checker_data[0])
        return res[0]["id"]


if __name__ == "__main__":
    c = CommentRequest(name="asd", url="asd", user_id=1, owner_id=1, item_id=3)
    l = LikeRequest(type="post", url="asd", user_id=1, owner_id=1, item_id=3)
    r = Request(url="asd", like=l, comment=c)
    # print(r.dict())
    res = Response(url=1, is_liked=True, is_commented=False)

    print(res)
