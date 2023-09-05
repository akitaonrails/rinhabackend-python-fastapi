import redis.asyncio as redis
import os
import logging
import pickle

logger = logging.getLogger("uvicorn")

CACHE_URL = os.getenv("CACHE_URL", "redis://redis:6379")

redis_client = None


async def connect(url=CACHE_URL):
    global redis_client
    pool = redis.ConnectionPool.from_url(url)
    redis_client = redis.Redis(connection_pool=pool)


async def close():
    global redis_client
    if redis_client:
        await redis_client.close()


async def insert_apelido(apelido):
    global redis_client
    if redis_client:
        await redis_client.set(f"apelido:{apelido}", 1)


async def apelido_exist(apelido):
    global redis_client
    if redis_client:
        person = await redis_client.get(f"apelido:{apelido}")
        return True if person else False


async def insert_person(id, person):
    global redis_client
    if redis_client:
        await redis_client.set(f"id:{id}", pickle.dumps(person))


async def get_person(id):
    global redis_client
    if redis_client:
        if person := await redis_client.get(f"id:{id}"):
            return pickle.loads(person)


async def insert_person_term(termo, person):
    global redis_client
    if redis_client:
        return await redis_client.setex(f"termo:{termo}", 60, pickle.dumps(person))


async def get_person_term(termo):
    global redis_client
    if redis_client:
        if people := await redis_client.get(f"termo:{termo}"):
            return pickle.loads(people)
