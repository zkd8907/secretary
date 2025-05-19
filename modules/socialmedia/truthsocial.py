import os
from datetime import datetime
from bs4 import BeautifulSoup
from truthbrush.api import Api
from modules.socialmedia.post import Post
from utils.redisclient import redis_client

api = Api()

print(f"TruthSocial API initialized, token: {api.auth_id}")


def fetch(user_id: str) -> list[Post]:
    last_post_id = redis_client.get(f"truthsocial:{user_id}:last_post_id")
    if last_post_id is None:
        last_post_id = '114344562778183288'
    else:
        last_post_id = str(last_post_id, encoding='utf-8')

    if os.getenv('DEBUG') == 'true':
        print(
            f"Fetching TruthSocial posts for user: {user_id} under debug mode, last_post_id will be set to 114344562778183288")
        last_post_id = '114344562778183288'

    posts = list(api.pull_statuses(username=user_id, since_id=last_post_id))

    noneEmptyPosts = []
    for post in posts:
        content = BeautifulSoup(post['content'], 'html.parser').get_text()
        if len(content) > 0:
            post['content'] = content
            post_time = datetime.strptime(
                post['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

            noneEmptyPosts.append(
                Post(post['id'], post_time, content, post['url'], post['account']['display_name'], post['account']['url']))

        if post['id'] > last_post_id:
            last_post_id = post['id']

    if os.getenv('DEBUG') == 'true':
        print(
            f"Fetching TruthSocial posts for user: {user_id} under debug mode, last_post_id will be updated")
    else:
        redis_client.set(f"truthsocial:{user_id}:last_post_id", last_post_id)

    return noneEmptyPosts


if __name__ == "__main__":
    user_id = "realDonaldTrump"
    posts = fetch(user_id)
    for post in posts:
        print(post['content'])
        print(post['created_at'])
