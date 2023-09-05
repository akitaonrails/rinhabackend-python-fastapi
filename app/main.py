from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.exceptions import RequestValidationError
from typing import List
from uuid import uuid4
import app.database as database
import app.models as models
import cachetools


app = FastAPI()

cache_apelido = cachetools.TTLCache(maxsize=50000,ttl=600)
cache_id = cachetools.TTLCache(maxsize=50000,ttl=600)
cache_termo = cachetools.TTLCache(maxsize=20000,ttl=60)

@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.post("/pessoas", status_code=201)
async def create_person(person: models.Person, response: Response):
    try:
        if cache_apelido.get(person.apelido):
            raise ValueError
        if await database.exists_by_apelido(person.apelido):
            raise ValueError

        person_id = str(uuid4())

        await database.insert_person(person_id, **person.model_dump())
        cache_id[person_id] = {"id":person_id, **person.model_dump()}
        cache_apelido[person.apelido] = 1
        response.headers["location"] = f"/pessoas/{person_id}"
        return 
    except ValueError:
        raise HTTPException(status_code=422)
    except Exception:
        raise HTTPException(status_code=422)


@app.get("/pessoas/{id}", response_model=models.PersonResponse)
async def read_person(id: str):
    if person:=cache_id.get(id):
        return person
    if person_data := await database.find_by_id(id):
        person = models.PersonResponse.from_db(**person_data)
        cache_id[person.id] = person
        return person
    else:
        raise HTTPException(status_code=404)


@app.get("/pessoas", response_model=List[models.PersonResponse])
async def search_people(term: str = Query(..., alias="t")):
    if people:=cache_termo.get(term):
        return people
    people_dto = await database.find_by_term(term)
    people = [
        models.PersonResponse.from_db(**person_data) for person_data in people_dto
    ]
    cache_termo[term] = people
    return people


@app.get("/contagem-pessoas")
async def count_people():
    count = await database.count_people()
    return str(count)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, handler):
    return Response(status_code=400)
