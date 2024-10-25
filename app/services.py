from redis import asyncio as aioredis
import json

async def first(objects):
    """Getting first object from the iterable object"""
    if len(objects) == 0:
        return None
    return objects[0]

async def _get_object(
    obj_field: str,
    obj_value: str | int,
    db: aioredis.Redis
) -> dict | None:
    """Getting object by field and value"""
    data = list(
        filter(
            lambda x: x[obj_field] == obj_value,
            map(
                lambda x: json.loads(x.decode()),
                db.lrange('objects', 0, -1)
            )
        )
    )
    return await first(data)

async def get_object_by_id(
    id: int,
    db: aioredis.Redis
) -> dict | None:
    """Getting object by id"""
    return await _get_object(
        'id', id, db
    )

async def get_object_by_uid(
    uid: str,
    db: aioredis.Redis
) -> dict | None:
    """Getting object by UID"""
    return await _get_object(
        'uid', uid, db
    )

async def create_object(data: dict, db: aioredis.Redis) -> dict:
    """Creating object in db"""
    serialized_data = json.dumps(data)
    db.lpush('objects', serialized_data)
    return data

async def get_objects(db: aioredis.Redis) -> list[dict]:
    """Getting objects from db"""
    data = db.lrange('objects', 0, -1)
    return [json.loads(i.decode()) for i in data]


