import redis

async def get_redis_connection() -> redis.Redis:
    """Connecting in db"""
    return redis.Redis(
        host='redis',
        port=6379,
        db=0,
        )


