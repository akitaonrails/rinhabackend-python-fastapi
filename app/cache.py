import redis.asyncio as redis
import os
import logging
import pickle

logger = logging.getLogger("uvicorn")

CACHE_URL = os.getenv("CACHE_URL", "redis://redis:6379")

redis_pool = None

async def connect(url=CACHE_URL):
    global redis_pool
    redis_pool = await redis.from_url(url)

async def close():
    global redis_pool
    if redis_pool:
        await redis_pool.close()

async def insert_apelido(apelido):
    global redis_pool
    if redis_pool:
        await redis_pool.set(f"apelido:{apelido}",1)

async def apelido_exist(apelido):
    global redis_pool
    if redis_pool:
        person = await redis_pool.get(f"apelido:{apelido}")
        return True if person else False
    
async def insert_person(id, person):
    global redis_pool
    if redis_pool:
        await redis_pool.set(f"id:{id}", pickle.dumps(person))

async def get_person(id):
    global redis_pool
    if redis_pool:
        if person := await redis_pool.get(f"id:{id}"):
            return pickle.loads(person)

async def insert_person_term(termo,person):
    global redis_pool
    if redis_pool:
        return await redis_pool.setex(f"termo:{termo}", 60, pickle.dumps(person))
 
async def get_person_term(termo):
    global redis_pool
    if redis_pool:
        if people:= await redis_pool.get(f"termo:{termo}"):
            return pickle.loads(people)