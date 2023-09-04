from fastapi import FastAPI
from fastapi.testclient import TestClient
from middleware import validateDate, validateBody, errorHandler
import pytest

app = FastAPI()

@app.middleware("http")
async def validate_request(request, call_next):
    is_valid = validateBody(request)
    if not is_valid:
        return {"message": "Invalid request body"}
    response = await call_next(request)
    return response

@app.post("/test/")
async def test_post(payload: dict):
    return {"message": "Success", "payload": payload}

client = TestClient(app)


def test_validate_date():
    assert validateDate("2021-09-04") == True
    assert validateDate("invalid-date") == False
    assert validateDate("2021-13-04") == False


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"apelido": "test", "nome": "Test", "nascimento": "2021-09-04", "stack": []}, 200),
        ({"apelido": "test", "nome": "Test", "nascimento": "2021-09-04", "stack": ["Python", "JavaScript"]}, 200),
        ({"apelido": "", "nome": "Test", "nascimento": "2021-09-04", "stack": ["Python", "JavaScript"]}, 422),
        ({"apelido": "test", "nome": "", "nascimento": "2021-09-04", "stack": ["Python", "JavaScript"]}, 422),
        ({"apelido": "test", "nome": "Test", "nascimento": "invalid-date", "stack": ["Python", "JavaScript"]}, 422),
    ],
)
def test_validate_body(payload, expected_status):
    response = client.post("/test/", json=payload)
    assert response.status_code == expected_status
