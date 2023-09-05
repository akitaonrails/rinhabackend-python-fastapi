import pytest
import asyncio
import app.database as database
import app.models as models
from uuid import uuid4


@pytest.mark.asyncio
async def test_insert_and_find_person():
    id = str(uuid4())
    apelido = "John"
    nome = "Doe"
    nascimento = "2000-01-01"
    stack = ["Python", "JavaScript"]

    person = models.Person(
        apelido=apelido, nome=nome, nascimento=nascimento, stack=stack
    )
    # Insert a person into the database
    await database.insert_person(id, **person.model_dump())

    # Retrieve the person from the database
    person_data = await database.find_by_id(id)
    person_response = models.PersonResponse.from_db(**person_data)

    assert person_data is not None
    assert person_response.apelido == apelido
    assert person_response.nome == nome
    assert str(person_response.nascimento) == nascimento
    assert person_response.stack == stack


@pytest.mark.asyncio
async def test_count_people():
    id1 = str(uuid4())
    person1 = models.Person(
        apelido="Alice", nome="Smith", nascimento="1990-05-01", stack=["Java"]
    )
    id2 = str(uuid4())
    person2 = models.Person(
        apelido="Bob", nome="Johnson", nascimento="1992-05-01", stack=["C++"]
    )

    await database.insert_person(id1, **person1.model_dump())
    await database.insert_person(id2, **person2.model_dump())

    count = await database.count_people()

    assert count >= 2


@pytest.mark.asyncio
async def test_find_by_term():
    id = str(uuid4())
    apelido = "search_test"
    nome = "Search Test"
    nascimento = "1980-01-01"
    stack = ["Python"]

    person = models.Person(
        apelido=apelido, nome=nome, nascimento=nascimento, stack=stack
    )

    await database.insert_person(id, **person.model_dump())

    results = await database.find_by_term("search")
    print(results)
    found = any(str(r["id"]) == id for r in results)

    assert found
