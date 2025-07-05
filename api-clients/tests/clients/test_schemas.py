from app.schemas import ClientCreate, ClientOut, Token


def test_client_create_schema():
    data = {
        "username": "client1",
        "firstName": "Alice",
        "lastName": "Doe",
        "name": "AliceDoe",
        "createdAt": "2024-07-01T00:00:00",
        "postalCode": "75000",
        "city": "Paris",
        "profileFirstName": "Alice",
        "profileLastName": "Doe",
        "companyName": "Company",
        "email": "alice@example.com"
    }
    client = ClientCreate(**data)
    assert client.username == "client1"
    assert client.email == "alice@example.com"


def test_token_schema():
    token = Token(access_token="abc123", token_type="bearer")
    assert token.access_token == "abc123"
    assert token.token_type == "bearer"
