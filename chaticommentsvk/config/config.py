import typing
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent


def load_yaml(file) -> dict:
    with open(Path(BASE_DIR, file), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_arg_yaml(file) -> dict:
    with open(Path(BASE_DIR, f"{file}.yml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Bot(BaseModel):
    token: str
    check_type: typing.Literal["like", "comment", "like_comment"]
    queue_length: int
    admins: Optional[list[int]]
    vip: Optional[list[int]]
    startup_clear: bool
    dd_messages: int


class Vk(BaseModel):
    token: str


class Database(BaseModel):
    storage: str
    host: str


class Config(BaseModel):
    bot: Bot
    vk: Vk
    db: Database


config = Config(**load_yaml("config.yml"))
