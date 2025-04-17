from tweety import Twitter
from utils.redisClient import redis_client
from modules.socialmedia.post import Post
app = Twitter('session')


def fetch(user_id: str) -> list[Post]:
    last_post_id = redis_client.get(f"tweet:{user_id}:last_post_id")

    if last_post_id is None:
        last_post_id = '0'
    else:
        last_post_id = str(last_post_id, encoding='utf-8')

    try:
        posts = app.get_tweets(user_id)
    except Exception as e:
        print(e)
        return []

    noneEmptyPosts = []

    for post in posts:
        if post.id > last_post_id:
            last_post_id = post.id
        else:
            continue

        if post.text:
            noneEmptyPosts.append(Post(post.id, post.created_on, post.text))

    redis_client.set(f"tweet:{user_id}:last_post_id", last_post_id)

    return noneEmptyPosts


if __name__ == "__main__":
    posts = fetch('myfxtrader')
    for post in posts:
        print(post.content)
