import os
import redis
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read Redis URL from environment variables
REDIS_URL = os.getenv("REDIS_URL")

# Initialize Redis client
redis_client = redis.from_url(REDIS_URL)


def test_redis_connection():
    try:
        redis_client.ping()
        print("Connected to Redis successfully!")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Uncomment the following line to test the connection when running this file directly
if __name__ == "__main__":
    test_redis_connection()
