from bs4 import BeautifulSoup
from truthbrush.api import Api

from utils.redisClient import redis_client

api = Api()


def fetch(user_id: str):
    last_post_id = None
    last_post_id = redis_client.get(f"truthsocial:{user_id}:last_post_id")
    last_post_id = str(last_post_id, encoding='utf-8')
    if last_post_id is None:
        last_post_id = '114344562778183288'

    posts = list(api.pull_statuses(username=user_id, since_id=last_post_id))

    noneEmptyPosts = []
    for post in posts:
        content = BeautifulSoup(post['content'], 'html.parser').get_text()
        if len(content) > 0:
            post['content'] = content
            noneEmptyPosts.append(post)

        if post['id'] > last_post_id:
            last_post_id = post['id']

    redis_client.set(f"truthsocial:{user_id}:last_post_id", last_post_id)

    return noneEmptyPosts


if __name__ == "__main__":
    user_id = "realDonaldTrump"
    posts = fetch(user_id)
    for post in posts:
        print(post['content'])
        print(post['created_at'])
