from datetime import datetime
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
        # Ensure post_on is in UTC time
        if post_on.tzinfo is None:
            post_on = pytz.UTC.localize(post_on)
        self.post_on = post_on
        self.content = content
        self.url = url
        self.poster_name = poster_name
        self.poster_url = poster_url

    def get_local_time(self) -> datetime:
        """Get time in local timezone"""
        # Get current timezone from operating system
        local_tz_name = time.tzname[0]  # Get current timezone name
        try:
            # Try to use the obtained timezone name
            local_tz = pytz.timezone(local_tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            # If timezone name cannot be recognized, use TZ environment variable
            tz_env = os.environ.get('TZ')
            if tz_env:
                try:
                    local_tz = pytz.timezone(tz_env)
                except pytz.exceptions.UnknownTimeZoneError:
                    # If timezone in environment variable cannot be recognized, use UTC
                    print(
                        f"Warning: Cannot recognize timezone '{tz_env}', using UTC timezone")
                    local_tz = pytz.UTC
            else:
                # If TZ environment variable is not set, use UTC
                print("Warning: TZ environment variable not set, using UTC timezone")
                local_tz = pytz.UTC

        return self.post_on.astimezone(local_tz)

    def get_dict(self) -> dict:
        """get the properties of current post as dict"""
        return {
            "id": self.id,
            "post_time": self.get_local_time().strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "post_url": self.url,
            "poster_name": self.poster_name,
            "poster_url": self.poster_url
        }

    def __str__(self) -> str:
        return f"Post(id={self.id}, post_on={self.post_on}, content={self.content}, url={self.url}, poster_name={self.poster_name}, poster_url={self.poster_url})"

    def __repr__(self) -> str:
        return self.__str__()
