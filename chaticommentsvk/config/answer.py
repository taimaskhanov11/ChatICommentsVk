from pydantic import BaseModel

from chaticommentsvk.config.config import load_yaml


class Common(BaseModel):
    link_exists: str
    incorrect_message: str
    no_access: str
    check_failed: str
    error: str


class Answer(BaseModel):
    common: Common


answer = Answer(**load_yaml("answers.yml"))
