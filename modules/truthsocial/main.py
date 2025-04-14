from truthbrush.api import Api
from dotenv import load_dotenv
import os

load_dotenv()

api = Api(
    username=os.getenv('TRUTH_SOCIAL_ACCOUNT'),
    password=os.getenv('TRUTH_SOCIAL_PASSWORD')
)


def fetch(user_id: str):
    posts = api.pull_statuses(username=user_id)
    return posts


if __name__ == "__main__":
    user_id = "realDonaldTrump"
    posts = fetch(user_id)
    for post in posts:
        print(post)
