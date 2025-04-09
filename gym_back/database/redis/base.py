import aioredis

from ...config import redis as redis_conf

redis = aioredis.from_url(f"redis://{redis_conf.host}:{redis_conf.port}")
