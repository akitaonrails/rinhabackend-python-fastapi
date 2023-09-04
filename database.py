import os
import asyncpg
import logging
from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger("uvicorn")

DATABASE_URL = os.getenv("DB_URL", "postgresql://localhost:password@localhost:5432/rinha-fastapi-dev")

pool = None

async def connect():
    global pool
    try:
        logger.info(f"Connecting to db {DATABASE_URL}")
        pool = await asyncpg.create_pool(DATABASE_URL, max_size=int(os.getenv("DB_POOL", 200)), timeout=10)
        await create_tables()
    except Exception as err:
        logger.error(f"An error occurred when connecting: {err}, retrying connection in 3 seconds")
        app.add_event_handler("startup", connect)

async def close():
    await pool.close()

async def create_tables():
    logger.info(f"Creating table 'pessoas' if not exists")
    async with pool.acquire() as conn:
        await conn.execute('''
        CREATE EXTENSION IF NOT EXISTS "pgcrypto";
        CREATE EXTENSION IF NOT EXISTS "pg_trgm";

        CREATE OR REPLACE FUNCTION generate_searchable(_nome VARCHAR, _apelido VARCHAR, _stack JSON)
        RETURNS TEXT AS $$
        BEGIN
        RETURN _nome || _apelido || _stack;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;

        CREATE TABLE IF NOT EXISTS pessoas (
            id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
            apelido TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            nascimento DATE NOT NULL,
            stack JSON,
            searchable TEXT GENERATED ALWAYS AS (generate_searchable(nome, apelido, stack)) STORED
        );

        CREATE INDEX IF NOT EXISTS idx_pessoas_searchable ON pessoas USING gist(searchable gist_trgm_ops);
        CREATE UNIQUE INDEX IF NOT EXISTS pessoas_apelido_index ON pessoas(apelido);
        ''')

async def insert_person(id, apelido, nome, nascimento, stack):
    async with pool.acquire() as conn:
        await conn.execute('''
        INSERT INTO pessoas(id, apelido, nome, nascimento, stack)
        VALUES ($1, $2, $3, $4, $5);
        ''', id, apelido, nome, nascimento, stack)

async def find_by_id(id):
    async with pool.acquire() as conn:
        result = await conn.fetchrow('''
        SELECT id, apelido, nome, to_char(nascimento, 'YYYY-MM-DD') as nascimento, stack
        FROM pessoas
        WHERE id = $1;
        ''', id)
        return result

async def find_by_term(term):
    async with pool.acquire() as conn:
        result = await conn.fetch('''
        SELECT id, apelido, nome, to_char(nascimento, 'YYYY-MM-DD') as nascimento, stack
        FROM pessoas
        WHERE searchable ILIKE $1
        LIMIT 50;
        ''', f"%{term}%")
        return result

async def exists_by_apelido(apelido):
    async with pool.acquire() as conn:
        result = await conn.fetchrow('''
        SELECT COUNT(1)
        FROM pessoas
        WHERE apelido = $1;
        ''', apelido)
        return result[0] > 0

async def count_people():
    async with pool.acquire() as conn:
        result = await conn.fetchrow('''
        SELECT COUNT(1)
        FROM pessoas;
        ''')
        return result[0]

app.add_event_handler("startup", connect)
