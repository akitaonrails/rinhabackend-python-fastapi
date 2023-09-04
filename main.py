from fastapi import FastAPI, Body, HTTPException, Query
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import List, Optional
import database
import os

app = FastAPI()

class Person(BaseModel):
    apelido: str = Field(..., max_length=32)
    nome: str = Field(..., max_length=100)
    nascimento: str
    stack: Optional[List[str]]

class PersonInDB(Person):
    id: str

@app.post("/pessoas/", status_code=201)
async def create_person(person: Person):
    try:
        if database.exists_by_apelido(person.apelido):
            raise HTTPException(status_code=422, detail="Apelido already exists")

        id = str(uuid4())
        await database.insert_person(id, **person.model_dump())
        return {"id": id, "location": f"/pessoas/{id}"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/pessoas/{id}/", response_model=PersonInDB)
async def read_person(id: str):
    person_data = await database.find_by_id(id)
    if person_data is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return PersonInDB(id=person_data["id"], **person_data)

@app.get("/pessoas/", response_model=List[PersonInDB])
async def search_people(term: str = Query(..., alias="t")):
    people = await database.find_by_term(term)
    return [PersonInDB(id=person_data["id"], **person_data) for person_data in people]

@app.get("/contagem-pessoas/")
async def count_people():
    count = await database.count_people()
    return {"count": count}
