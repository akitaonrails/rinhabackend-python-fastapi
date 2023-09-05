import pytest
import asyncio
import app.database as database
import app.cache as cache


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module", autouse=True)
async def setup_db(event_loop):
    await database.connect(url="postgresql://user:pass@localhost:5432/rinha")
    yield
    await database.close()

@pytest.fixture(scope="module", autouse=True)
async def setup_cache(event_loop):
    await cache.connect(url="redis://localhost:6379")
    yield
    await cache.close()
