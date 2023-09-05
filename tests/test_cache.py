import pytest
import asyncio
import app.cache as cache
import app.models as models
from uuid import uuid4


@pytest.mark.asyncio
async def test_set_and_get_person():
    id = str(uuid4())
    apelido = "John"
    nome = "Doe"
    nascimento = "2000-01-01"
    stack = ["Python", "JavaScript"]

    person = models.Person(
        apelido=apelido, nome=nome, nascimento=nascimento, stack=stack
    )
    # Insert a person into the cache
    await cache.insert_person(id, person)

    # Retrieve the person from the cache
    person_data = await cache.get_person(id)

    assert person_data is not None
    assert person_data.apelido == apelido
    assert person_data.nome == nome
    assert str(person_data.nascimento) == nascimento
    assert person_data.stack == stack

@pytest.mark.asyncio
async def test_set_and_get_apelido():
    apelido = "John"
    
    # Insert a person into the database
    await cache.insert_apelido(apelido)

    # Retrieve the person from the database
    cached_apelido = await cache.apelido_exist(apelido)

    assert cached_apelido is not None
    assert cached_apelido == True

@pytest.mark.asyncio
async def test_find_by_term():
    person1 = models.PersonResponse(
        id=str(uuid4()), apelido="Alice", nome="Smith", nascimento="1990-05-01", stack=["Python"]
    )
    person2 = models.PersonResponse(
        id=str(uuid4()), apelido="Bob", nome="Johnson", nascimento="1992-05-01", stack=["Python"]
    )

    people_response = [person1,person2]

    await cache.insert_person_term("ytho", people_response)
    cached_termo = await cache.get_person_term("ytho")

    assert cached_termo is not None
    assert len(cached_termo) == 2
    assert cached_termo == people_response
