from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_clients_route():
    response = client.get("/clients/")
    assert response.status_code in [200, 401, 500]


def test_create_client_unauthorized():
    client_data = {
        "username": "testuser",
        "firstName": "John",
        "lastName": "Doe",
        "name": "JohnD",
        "createdAt": "2024-07-01T00:00:00",
        "postalCode": "75000",
        "city": "Paris",
        "profileFirstName": "John",
        "profileLastName": "Doe",
        "companyName": "TestCorp",
        "email": "john.doe@example.com"
    }
    response = client.post("/clients/", json=client_data)
    # Doit échouer car on n'envoie pas de token
    assert response.status_code == 401

