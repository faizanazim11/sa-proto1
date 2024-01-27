from redis import Redis

from scripts.config import Databases

redis_connection = Redis.from_url(Databases.REDIS_URI, decode_responses=True)
