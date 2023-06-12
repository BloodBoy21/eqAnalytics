import asyncio
from services.streaming_service import init_consumer
from shared.mongo import database as mongo_db
from shared.db import engine, db


async def init():
    db.metadata.create_all(bind=engine, checkfirst=True)
    await mongo_db.client.start_session()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    init_consumer()
