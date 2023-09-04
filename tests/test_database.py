import pytest
import asyncio
import database
from uuid import uuid4

@pytest.mark.asyncio
async def test_insert_and_find_person():
    id = str(uuid4())
    apelido = "John"
    nome = "Doe"
    nascimento = "2000-01-01"
    stack = ["Python", "JavaScript"]

    # Insert a person into the database
    await database.insert_person(id, apelido, nome, nascimento, stack)

    # Retrieve the person from the database
    person_data = await database.find_by_id(id)

    assert person_data is not None
    assert person_data["apelido"] == apelido
    assert person_data["nome"] == nome
    assert person_data["nascimento"] == nascimento
    assert person_data["stack"] == stack

@pytest.mark.asyncio
async def test_count_people():
    id1 = str(uuid4())
    id2 = str(uuid4())

    await database.insert_person(id1, "Alice", "Smith", "1990-05-01", ["Java"])
    await database.insert_person(id2, "Bob", "Johnson", "1992-05-01", ["C++"])

    count = await database.count_people()

    assert count >= 2

@pytest.mark.asyncio
async def test_find_by_term():
    id = str(uuid4())
    apelido = "search_test"
    nome = "Search Test"
    nascimento = "1980-01-01"
    stack = ["Python"]

    await database.insert_person(id, apelido, nome, nascimento, stack)

    results = await database.find_by_term("search")
    found = any(r["id"] == id for r in results)

    assert found
