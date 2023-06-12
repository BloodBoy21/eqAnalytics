from confluent_kafka import Consumer, KafkaError, KafkaException
from aiokafka import AIOKafkaConsumer
import asyncio
from configs.earthquakeKafka import get_conf
from services.earthquake_service import EarthquakeService

EarthquakeService = EarthquakeService.get_instance()


async def consume():
    conf = get_conf()
    consumer = AIOKafkaConsumer(
        conf.get("topics"),
        bootstrap_servers=conf.get("bootstrap.servers"),  # type: ignore
        group_id=conf.get("group.id"),
    )
    await consumer.start()

    try:
        # Continuously consume messages
        async for message in consumer:
            # Process each message
            topic = message.topic
            data = message.value if message else ""
            data = str(data, "utf-8")  # type: ignore
            services = {"earthquake": EarthquakeService}
            services[topic].consume(data)

    finally:
        await consumer.stop()


def init_consumer():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
