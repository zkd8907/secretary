import os
from tweety import Twitter
from utils.redisclient import redis_client
from modules.socialmedia.post import Post
from dotenv import load_dotenv

load_dotenv()

twitter_session = os.getenv('TWITTER_SESSION')
if twitter_session and twitter_session.strip():
    with open('session.tw_session', 'w') as f:
        f.write(twitter_session)

app = Twitter('session')
app.connect()

if (app.me is None):
    app.sign_in(os.getenv('TWITTER_USERNAME'), os.getenv('TWITTER_PASSWORD'))


def fetch(user_id: str) -> list[Post]:
    cursor = redis_client.get(f"twitter:{user_id}:last_post_id")

    if cursor is None:
        cursor = ''
    else:
        cursor = str(cursor, encoding='utf-8')

    if os.getenv('DEBUG') == 'true':
        print(
            f"Fetching Twitter posts for user: {user_id} under debug mode, cursor will be set to empty")
        cursor = ''

    try:
        posts = app.get_tweets(user_id, cursor=cursor)
    except Exception as e:
        print(e)
        return []

    noneEmptyPosts = []

    for post in posts:
        if 'tweets' in post:
            latest_id = None
            latest_created_on = None
            combined_text = ""
            latest_url = ""
            poster = None

            for tweet in post.tweets:
                if tweet.text:
                    combined_text += tweet.text + "\n"
                if latest_created_on is None or tweet.created_on > latest_created_on:
                    latest_created_on = tweet.created_on
                    latest_id = tweet.id
                    latest_url = tweet.url
                    poster = tweet.author

            if combined_text and latest_id and latest_created_on and poster:
                noneEmptyPosts.append(
                    Post(latest_id, latest_created_on, combined_text.strip(), latest_url, poster.name, poster.profile_url))
        elif post.text:
            noneEmptyPosts.append(Post(post.id, post.created_on, post.text,
                                  post.url, post.author.name, post.author.profile_url))

    if os.getenv('DEBUG') == 'true':
        print(
            f"Fetching Twitter posts for user: {user_id} under debug mode, cursor will be updated")
    else:
        redis_client.set(f"twitter:{user_id}:last_post_id", posts.cursor_top)

    return noneEmptyPosts


if __name__ == "__main__":
    posts = fetch('myfxtrader')
    for post in posts:
        print(post.content)
