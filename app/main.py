from typing import Annotated
import logging

import redis
from aiohttp import ClientSession
from fastapi import FastAPI, HTTPException, Depends, Body
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge, Counter
from starlette.responses import Response

from tasks import persist_task
from schemas import LocationSchema
from schemas import TaskSchemaBase
from database import get_redis_connection
from services import get_object_by_id, get_objects, create_object


app = FastAPI()

processing_time = Gauge(
    "task_event_process_duration",
    "Time it took to complete a task"
)

# Создаем метрику Counter для количества выполненных задач с метками
processed_counter = Counter(
    "task_event_processing_total",
    "How many tasks have been processed",
    ["task"]
)


@app.get('/ping')
async def ping():
    return 'pong'

@app.post("/objects/", response_model=dict)
async def create_new_object(data: dict, db: redis.Redis = Depends(get_redis_connection)):
    return await create_object(data, db)

@app.get("/objects/", response_model=list[dict])
async def read_objects(db: redis.Redis = Depends(get_redis_connection)):
    return await get_objects(db)

@app.get("/objects/{id}", response_model=dict)
async def read_object_by_id(id: int, db: redis.Redis = Depends(get_redis_connection)):
    obj = await get_object_by_id(id, db)
    if obj is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj

@app.post("/tasks/")
async def create_new_task(
        task: TaskSchemaBase,
        location: Annotated[
            LocationSchema, Body()
        ],
        db: Annotated[
            redis.Redis,
            Depends(get_redis_connection)
        ]
):
    async with ClientSession() as session:
        async with session.post(
                url="http://locations:8081/locations/",
                json=location.dict()
        ) as response:
            if response.ok:
                new_location = await response.json()
            else:
                new_location = None
                logging.error(msg="Error returned from LocationServiceAPI"
                                  f"{response.text()}")
    task.location = new_location
    new_task = await create_object(
        task.dict(), db
    )
    if new_task:
        processing_time.set(2.5)
        processed_counter.labels(task=task.name).inc()
        persist_task(db, task)
    return new_task


@app.get("/metrics")
def get_metrics():
    metrics = generate_latest()
    return Response(metrics, media_type=CONTENT_TYPE_LATEST)