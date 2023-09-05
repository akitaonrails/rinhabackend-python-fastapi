from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List
from uuid import uuid4
import app.database as database
import app.models as models


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.post("/pessoas", status_code=201)
async def create_person(person: models.Person, response: Response):
    try:
        if await database.exists_by_apelido(person.apelido):
            raise ValueError

        person_id = uuid4()

        await database.insert_person(person_id, **person.model_dump())
        response.headers["location"] = f"/pessoas/{person_id}"
        return {"id": str(person_id)}
    except ValueError:
        raise HTTPException(status_code=422, detail="Apelido already exists")
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/pessoas/{id}", response_model=models.PersonResponse)
async def read_person(id: str):
    person_data = await database.find_by_id(id)
    if person_data is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return models.PersonResponse.from_db(**person_data)


@app.get("/pessoas", response_model=List[models.PersonResponse])
async def search_people(term: str = Query(..., alias="t")):
    people = await database.find_by_term(term)
    return [models.PersonResponse.from_db(**person_data) for person_data in people]


@app.get("/contagem-pessoas")
async def count_people():
    count = await database.count_people()
    return str(count)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, handler):
    return JSONResponse({"detail": "Bad Request"}, status_code=400)
