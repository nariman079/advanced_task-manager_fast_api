

from redis import asyncio as aioredis
import asyncio
import logging

from prometheus_client import CollectorRegistry, Counter, push_to_gateway

logging.basicConfig(level=logging.INFO)

async def process_stream():
    registry = CollectorRegistry()

    client = await aioredis.from_url("redis://redis:6379/0")
    logging.info(msg="Connecting to redis")
    stream = "task-stream"
    consumer_group = "consumer_group"
    consumer = "consumer_name"

    try:
        await client.xgroup_create(stream, consumer_group, '0', mkstream=True)
        logging.info(msg="Create group")
        print("Create group")
    except aioredis.ResponseError as error:
        if "BUSYGROUP Consumer Group name already exists" not in str(error):
            raise error
    received_messages_from_stream = Counter(
        'received_messages_from_stream',
        "Полученные сообшения в Redis Stream",
        registry=registry
    )
    while True:
        try:
            entries = await client.xreadgroup(
                groupname=consumer_group,
                consumername=consumer,
                streams={stream: '>'},
                count=1,
                block=0,
                noack=False
            )

            if entries:
                _, messages = entries[0]

                for message in messages:
                    received_messages_from_stream.inc()
                    message_id = message[0]
                    values = message[1]

                    task_id = values.get(b'task_id')
                    timestamp = values.get(b'timestamp')
                    location_id = values.get(b'location_id')
                    print(f"Received {task_id} {timestamp} {location_id}")
                    logging.info(f"Received {task_id} {timestamp} {location_id}")
                    await client.xack(stream, consumer_group, message_id)
                    push_to_gateway('push-gateway:9091', job='push-gateway', registry=registry)
        except Exception as e:
            logging.error(f"Error: {e}")

asyncio.run(process_stream())
