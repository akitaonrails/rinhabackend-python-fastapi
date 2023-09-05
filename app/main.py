from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List
from uuid import uuid4
import app.database as database
import app.cache as cache
import app.models as models


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await database.connect()
    await cache.connect()


@app.post("/pessoas", status_code=201)
async def create_person(person: models.Person, response: Response):
    try:
        if await cache.apelido_exist(person.apelido):
            raise ValueError

        person_id = uuid4()

        await cache.insert_apelido(person.apelido)
        await database.insert_person(person_id, **person.model_dump())
        await cache.insert_person(
            str(person_id),
            models.PersonResponse(id=str(person_id), **person.model_dump()),
        )
        response.headers["location"] = f"/pessoas/{person_id}"
        return {"id": str(person_id)}
    except ValueError:
        raise HTTPException(status_code=422, detail="Apelido already exists")
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/pessoas/{id}", response_model=models.PersonResponse)
async def read_person(id: str):
    if person := await cache.get_person(id):
        return person
    elif person_data := await database.find_by_id(id):
        person = models.PersonResponse.from_db(**person_data)
        await cache.insert_person(id, person)
        return person
    else:
        raise HTTPException(status_code=404, detail="Person not found")


@app.get("/pessoas", response_model=List[models.PersonResponse])
async def search_people(term: str = Query(..., alias="t")):
    if people := await cache.get_person_term(term):
        return people
    people = await database.find_by_term(term)
    people_response = [
        models.PersonResponse.from_db(**person_data) for person_data in people
    ]
    await cache.insert_person_term(term, people_response)
    return people_response


@app.get("/contagem-pessoas")
async def count_people():
    count = await database.count_people()
    return str(count)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, handler):
    return JSONResponse({"detail": "Bad Request"}, status_code=400)
