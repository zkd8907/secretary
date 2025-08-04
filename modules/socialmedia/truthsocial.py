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

    raw_posts = list(api.pull_statuses(username=user_id, since_id=last_post_id))

    processed_posts = []
    for post_data in raw_posts:
        content = BeautifulSoup(post_data['content'], 'html.parser').get_text()
        if len(content) > 0:
            post_data['content'] = content
            post_time = datetime.strptime(
                post_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

            processed_posts.append(
                Post(post_data['id'], post_time, content, post_data['url'], post_data['account']['display_name'], post_data['account']['url']))

        if post_data['id'] > last_post_id:
            last_post_id = post_data['id']

    if os.getenv('DEBUG') == 'true':
        print(
            f"Fetching TruthSocial posts for user: {user_id} under debug mode, last_post_id will be updated")
    else:
        redis_client.set(f"truthsocial:{user_id}:last_post_id", last_post_id)

    return processed_posts


if __name__ == "__main__":
    user_id = "realDonaldTrump"
    posts = fetch(user_id)
    for post in posts:
        print(post['content'])
        print(post['created_at'])
