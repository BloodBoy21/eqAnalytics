import os
from dotenv import load_dotenv

if os.getenv("ENV") != "production":
    load_dotenv()


KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "0.0.0.0")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")
KAFKA_TOPICS = os.environ.get("KAFKA_TOPICS", "earthquake")
conf = {
    "bootstrap.servers": KAFKA_SERVER + ":" + KAFKA_PORT,
    "group.id": "earthquake-consumer",
    "auto.offset.reset": "smallest",
    "topics": KAFKA_TOPICS.split(","),
}


def get_conf():
    return conf
