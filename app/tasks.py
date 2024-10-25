import uuid
import time
from dataclasses import dataclass, asdict

import redis

from schemas import TaskSchemaBase


@dataclass
class TaskMessage:
    name: str
    task_id: str | None
    timestamp: int | None
    location: str | None = None

    def __post_init__(self):
        self.timestamp = int(time.time())
        self.task_id = str(uuid.uuid4())

def publish(
        client: redis.Redis,
        message: TaskMessage
):
    """Publish task in redis-client"""
    message.location = "default"
    cmd = client.xadd("task-stream", asdict(message))

    return cmd


def persist_task(redis_client: redis.Redis, task_schema: TaskSchemaBase):
    """Task preparation before send in Redis"""
    values = task_schema.dict()
    values["location"] = "default" # Clear location initially
    task = TaskMessage(**task_schema.dict(), timestamp=None, task_id=None)
    hmset_result = redis_client.hset(f'{task.task_id}', mapping=values)
    if hmset_result is None:
        return "Error in HSET"
    zadd_result = redis_client.zadd("tasks", {task.task_id: task.timestamp})
    if zadd_result is None:
        return "Error in ZADD"

    return publish(redis_client, task)
