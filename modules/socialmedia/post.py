from datetime import datetime
from typing import Optional


class Post:
    def __init__(
        self,
        id: str,
        post_on: datetime,
        content: str,
        url: str,
        poster_name: str,
        poster_url: str
    ):
        self.id = id
        self.post_on = post_on
        self.content = content
        self.url = url
        self.poster_name = poster_name
        self.poster_url = poster_url

    def __str__(self) -> str:
        return f"Post(id={self.id}, post_on={self.post_on}, content={self.content}, url={self.url}, poster_name={self.poster_name}, poster_url={self.poster_url})"

    def __repr__(self) -> str:
        return self.__str__()
