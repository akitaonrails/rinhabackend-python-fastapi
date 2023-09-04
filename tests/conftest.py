import pytest
import asyncio
import database

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module", autouse=True)
async def setup_db(event_loop):
    await database.connect()
    yield
    await database.close()
