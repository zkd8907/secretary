from datetime import datetime
from typing import Optional


class Post:
    def __init__(
        self,
        id: str,
        post_on: datetime,
        content: str
    ):
        self.id = id
        self.post_on = post_on
        self.content = content

    def __str__(self) -> str:
        return f"Post(id={self.id}, post_on={self.post_on}, content={self.content})"

    def __repr__(self) -> str:
        return self.__str__()
