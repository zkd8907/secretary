from datetime import datetime
from typing import Optional
import pytz
import time
import os


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
        # 确保 post_on 是 UTC 时间
        if post_on.tzinfo is None:
            post_on = pytz.UTC.localize(post_on)
        self.post_on = post_on
        self.content = content
        self.url = url
        self.poster_name = poster_name
        self.poster_url = poster_url

    def get_local_time(self) -> datetime:
        """获取本地时区的时间"""
        # 从操作系统获取当前时区
        local_tz_name = time.tzname[0]  # 获取当前时区名称
        try:
            # 尝试使用获取到的时区名称
            local_tz = pytz.timezone(local_tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            # 如果无法识别时区名称，则使用系统环境变量TZ
            tz_env = os.environ.get('TZ')
            if tz_env:
                try:
                    local_tz = pytz.timezone(tz_env)
                except pytz.exceptions.UnknownTimeZoneError:
                    # 如果环境变量中的时区也无法识别，则使用UTC
                    print(f"警告：无法识别时区 '{tz_env}'，使用UTC时区")
                    local_tz = pytz.UTC
            else:
                # 如果没有设置TZ环境变量，则使用UTC
                print("警告：未设置TZ环境变量，使用UTC时区")
                local_tz = pytz.UTC

        return self.post_on.astimezone(local_tz)

    def __str__(self) -> str:
        return f"Post(id={self.id}, post_on={self.post_on}, content={self.content}, url={self.url}, poster_name={self.poster_name}, poster_url={self.poster_url})"

    def __repr__(self) -> str:
        return self.__str__()
