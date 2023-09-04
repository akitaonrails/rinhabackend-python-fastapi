from fastapi.testclient import TestClient
from main import app
from uuid import UUID
import json

client = TestClient(app)

def test_create_person():
    data = {
        "apelido": "test_apelido",
        "nome": "test_nome",
        "nascimento": "1992-05-23",
        "stack": ["Python", "FastAPI"]
    }
    response = client.post("/pessoas", json=data)
    assert response.status_code == 201
    location = response.headers.get("Location")
    assert location is not None
    id_str = location.split('/')[-1]
    assert UUID(id_str)  # Validate it's a UUID

def test_get_person_by_id():
    # Assuming you have an ID from the database, replace 'some_id' with it
    some_id = "your_uuid_here"
    response = client.get(f"/pessoas/{some_id}")
    assert response.status_code == 200
    person = response.json()
    assert 'id' in person

def test_find_by_term():
    term = "test"
    response = client.get("/pessoas", params={"t": term})
    assert response.status_code == 200
    people = response.json()
    assert isinstance(people, list)

def test_get_count():
    response = client.get("/contagem-pessoas")
    assert response.status_code == 200
    count = response.json()
    assert 'count' in count
